import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import regex as re

URL = 'https://www.fusecambridge.com/fuse-cambridge-ma/floorplans'
# URL = 'https://www.luxealewife.com/luxe-at-alewife-cambridge-ma/floorplans'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
divs = soup.find_all("div", recursive=True)
data = pd.DataFrame(columns= ["FloorPlan","BedBath","Price","sqft"])

for div in divs:
    div0 = div.find_all("div",class_="floorplan-info text-center")
    for div1 in div0:
        floorPlan = div1.find(class_="title")
        bedBath = div1.find(class_="bedbath")
        price = div1.find(class_="price").find("strong")
        sqft = div1.find(class_="sqft").find("strong")
        data.loc[data.size] = {"FloorPlan":floorPlan,"BedBath":bedBath, "Price":price, "sqft":sqft}

data.drop_duplicates(inplace=True)
data.index = np.arange(len(data))

print(data)
