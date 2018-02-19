from bs4 import BeautifulSoup
import requests

main_link = "https://www.postnummerservice.se/information/svenska-postnummer-och-postorter"
modified_link = "./modified.html"

global_dict = {}
num_of_requests = 0

def getSoupFrom(link):
    global num_of_requests
    num_of_requests += 1
    r = requests.get(link)
    link_data = r.text
    return BeautifulSoup(link_data, 'html5lib')

def main():
    main_link_soup = getSoupFrom(main_link)
    laens = main_link_soup.find_all('a', {"class": "imagemap_link"})
    for laen in laens:
        laen_link = laen['href']
        laenSoup = getSoupFrom(laen_link)
        handleLaen(laenSoup)

def handleKommun(kommun_soup):
    kommun_name = kommun_soup.select('h2')[0].text
    rows = kommun_soup.select('table')[0].find_all('tr')
    lowest_postalcode = rows[-2].find_all('td')[-1].text.replace(' ', '')
    highest_postalcode = rows[-1].find_all('td')[-1].text.replace(' ', '')
    global_dict[kommun_name] = (int(lowest_postalcode), int(highest_postalcode))
    print(kommun_name, ' - ', global_dict[kommun_name])

def handleLaen(laenSoup):
    for li in laenSoup.select('li.p5'):
        kommun_link = li.a['href']
        kommun_soup = getSoupFrom(kommun_link)
        handleKommun(kommun_soup)

main()
print('Number of requests : ', num_of_requests)
