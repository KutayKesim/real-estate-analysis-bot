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
    #newest-GRID
rightmove = "https://www.onthemarket.com/for-sale/property/london/?view=grid"
response = get(rightmove, headers=headers) #200 should be fine

page_html = BeautifulSoup(response.text, 'html.parser')
house_containers = page_html.find_all('li', class_="result property-result panel exclusive new first") #for each listing

prices = []
house_types = []
location = []

for container in house_containers:
    price = container.find_all('a', class_="price")[0].text
    prices.append(price)
    house_type = container.find_all('span', class_="title")[0].text
    house_types.append(house_type)
    loc = container.find_all('span', class_="address")[0].text
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
    var = var.replace('offersinexcessof', '')
    var = var.replace('guideprice', '')
    var = int(''.join(itertools.takewhile(str.isdigit, var))) #itertools for string to integer
    price_cleared.append(var)

for var in house_types:
    var = var.replace(' for sale', '')
    var = var.replace('\n', '')
    var = var.replace('  ', '')
    var = var.replace(' -', '')
    house_types_cleared.append(var)
for var in location:
    var = var.replace('\n', '')
    var = var.replace('\r', '')
    location_cleared.append(var)

#string to integer
#intlist = []
#for s in price_cleared:
    #intlist.append(int(s))

df_price = pd.DataFrame(price_cleared)
df_housetypes = pd.DataFrame(house_types_cleared)
df_location = pd.DataFrame(location_cleared)
print(df_price.describe())
