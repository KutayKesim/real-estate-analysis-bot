#! /usr/bin/python
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import itertools
import time
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
#! /usr/bin/python
headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

#newest-GRID
rightmove = "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E87490&sortType=6&includeSSTC=false&viewType=GRID"
response = get(rightmove, headers=headers) #200 should be fine


page_html = BeautifulSoup(response.text, 'html.parser')
house_containers = page_html.find_all('div', class_="propertyCard-wrapper")

prices = []
house_types = []
location = []

for container in house_containers:
    price = container.find_all('div', class_="propertyCard-priceValue")[0].text
    prices.append(price)
    house_type = container.find_all('h2')[0].text
    house_types.append(house_type)
    loc = container.find_all('address', class_="propertyCard-address")[0].text
    location.append(loc)

#clear the data
price_cleared = []
house_types_cleared = []
location_cleared = []

for var in prices:
    var = var.replace('\n', '')
    var = var.replace('£', '')
    var = var.replace(',', '')
    var = var.replace(' ', '')
    var = var.replace('Offersinregionof', '')
    price_cleared.append(var)

for var in house_types:
    var = var.replace(' for sale', '')
    var = var.replace('\n', '')
    var = var.replace('  ', '')
    house_types_cleared.append(var)

for var in location:
    var = var.replace('\n', '')
    var = var.replace('\r', '')
    location_cleared.append(var)

#string to integer
intlist = []
for s in price_cleared:
    intlist.append(int(s))

df_price = pd.DataFrame(intlist)
df_housetypes = pd.DataFrame(house_types_cleared)
df_location = pd.DataFrame(location_cleared)
print(df_price.describe())
df = pd.concat([df_price, df_housetypes, df_location])
df = pd.Dataframe.merge([df_price,df_housetypes,df_location], left_index=True)


df_price.to_csv(r'price.csv')
df_location.to_csv(r'location.csv')
df_housetypes.to_csv(r'housetypes.csv')
