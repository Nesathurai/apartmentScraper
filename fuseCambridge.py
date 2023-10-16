import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import regex as re

# URL = 'https://www.fusecambridge.com/fuse-cambridge-ma/floorplans'
# page = requests.get(URL)
# soup = BeautifulSoup(page.content, 'html.parser')
# divs = soup.find_all("div", recursive=True)
# data = pd.DataFrame(columns= ["FloorPlan","BedBath","Price","sqft"])

# for div in divs:
#     apartments = div.find_all("div",class_="tabs-content super-tab-content")
#     for floorplan in apartments:

#         floorPlan = floorplan.find(class_="title")
#         bedBath = floorplan.find(class_="bedbath")
#         price = floorplan.find(class_="price").find("strong")
#         sqft = floorplan.find(class_="sqft").find("strong")
#         data.loc[data.size] = {"FloorPlan":floorPlan,"BedBath":bedBath, "Price":price, "sqft":sqft}

# data.dropna(how="all", inplace=True)
# data.drop_duplicates(inplace=True)
# data.fillna("-", inplace=True)
# data.index = np.arange(len(data))

# print(data)

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import numpy as np
import regex as re


import time
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36')

# Set path to chromedriver as per your configuration
homedir = os.path.expanduser("~")
webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

# Choose Chrome Browser
browser = webdriver.Chrome( service=webdriver_service, options=chrome_options)
URL = 'https://www.fusecambridge.com/fuse-cambridge-ma/floorplans'
browser.get(URL)

# time.sleep(10)
# browser.save_screenshot("screenshot.png")
soup = BeautifulSoup(browser.page_source,"html.parser")
divs = soup.find_all("div", recursive=True)
# print(soup.prettify())
data = pd.DataFrame(columns= ["FloorPlan","BedBath","Price","sqft"])

for div in divs:
    tabs = div.find_all(id=re.compile("super-panel-.*"))
    for tab in tabs:
        apartments = tab.find_all(class_="floorplan-info text-center")
        for apartment in apartments:
            floorPlan = apartment.find(class_="title")
            if floorPlan:
                floorPlan = floorPlan.text.strip()
            bedBath = apartment.find(class_="bedbath")
            if bedBath:
                bedBath = bedBath.text.strip().replace("Bedroom","").replace("Bathroom","").replace(" | ","/ ")
            price = apartment.find(class_="price").find("strong")
            if price.string:
                price = price.text.strip()
            sqft = apartment.find(class_="sqft").find("strong")
            if sqft.string:
                sqft = sqft.string.strip()
            data.loc[data.size] = {"FloorPlan":floorPlan,"BedBath":bedBath, "Price":price, "sqft":sqft}

data.dropna(how="all", inplace=True)
data.drop_duplicates(inplace=True)
data.fillna("-", inplace=True)
data.index = np.arange(len(data))

print(data)
# data.to_excel("apartmentPrices.xlsx", "fuseCambridge")
with pd.ExcelWriter('apartmentPrices.xlsx', engine='openpyxl', mode='w') as writer:  
    data.to_excel(writer, sheet_name='fuseCambridge')


