#! /usr/bin/python
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
#! /usr/bin/python
headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

#newest100
zoopla = "https://www.zoopla.co.uk/for-sale/property/london/?q=London&results_sort=newest_listings&search_source=for-sale&page_size=100"
response = get(zoopla, headers=headers) #200 should be fine


page_html = BeautifulSoup(response.text, 'html.parser')
house_containers = page_html.find_all('li', class_="srp clearfix") #her bir listing icin

prices = []
house_types = []
location = []

for container in house_containers:
    price = container.find_all('a', class_="listing-results-price text-price")[0].text
    prices.append(price)
    house_type = container.find_all('a', style="text-decoration:underline;")[0].text
    house_types.append(house_type)
    loc = container.find_all('a', class_="listing-results-address")[0].text
    location.append(loc)

#clears the price data till integer is left
price_cleared = []
for var in prices:
    var = var.replace('\n', '')
    var = var.replace('Offers over', '')
    var = var.replace('Guide price', '')
    var = var.replace('£', '')
    var = var.replace(',', '')
    var = var.replace('From', '')
    var = var.replace('POA', '')
    var = var.replace('Fixed price', '')
    var = var.replace(' ', '')
    var = var.replace('Offersinregionof', '')
    price_cleared.append(var)

bed = []
htype = []
for var in house_types:
    var = var.replace(' for sale', '') #clear the list
    splitlist = var.split()
    if splitlist[0] == splitlist[-1]:
        bed.append('0')
        htype.append(splitlist[-1])
    else:
        bed.append(splitlist[0]) #grab the first item of list number of beds
        htype.append(splitlist[-1]) #grab the latest item of the list, type of the property

#string to integer
intlist = []
for s in price_cleared:
    intlist.append(int(s))

#convert to DataFrame
df_price = pd.DataFrame(intlist)
df_housetypes = pd.DataFrame(htype)
df_bed = pd.DataFrame(bed)
df_location = pd.DataFrame(location)
print(df_price.describe())
