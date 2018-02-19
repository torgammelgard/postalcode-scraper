from bs4 import BeautifulSoup
import requests

#global params
base_search_link = 'https://www.postnummerservice.se/adressoekning'
params = {'external': '0', 'street': '', 'postalcode': '', 'locality': '', 'county_code': '', 'submit': ''}

### gets data from www.postnummerservice.se
def lookup_data(params):
    r = requests.get(base_search_link, params)
    data = r.text
    return BeautifulSoup(data, "html5lib")

def find_kommun_name(postalcode):
    params['postalcode'] = postalcode
    soup = lookup_data(params)
    # find the last column in the first row of the table
    return soup.find('table').find('tbody').find('tr').find_all('td')[-1].text

print(find_kommun_name('13552'))
