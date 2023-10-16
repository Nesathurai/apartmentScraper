import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import regex as re

import time
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# import undetected_chromedriver as uc


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

# Get page
# browser.get("https://www.windsoratcambridgepark.com/floorplans/c")
# browser.get("https://www.windsorcommunities.com/properties/windsor-at-cambridge-park/")
# URL = 'https://www.luxealewife.com/luxe-at-alewife-cambridge-ma/floorplans'
URL = 'https://luxealewife.securecafe.com/onlineleasing/hanover-cambridge-park-a/floorplans.aspx?_ga=2.143208368.402136862.1697296183-589212948.1695917595'
# URL = 'https://hanovernorthcambridge.securecafe.com/onlineleasing/hanover-north-cambridge/floorplans.aspx?nocache=1'
browser.get(URL)

# time.sleep(10)
# browser.save_screenshot("screenshot.png")
soup = BeautifulSoup(browser.page_source,"html.parser")
divs = soup.find_all("div", recursive=True)
# print(soup.prettify())
data = pd.DataFrame(columns= ["FloorPlan","BedBath","Price","sqft"])

for div in divs:
    floorplans = div.find_all(class_=re.compile("floorplan-details"))
    for floorplan in floorplans:
        # print(floorplan.prettify())
        apartments = floorplan.find_all(attrs={"data-selenium-id":re.compile("tRow.*")})
        # print(len(apartments))
        for apartment in apartments:
            # print(apartment.prettify())
            floorPlan = apartment.find(attrs={"data-label":"Floor Plan"})
            if floorPlan:
                floorPlan = floorPlan.text.strip().replace("Floor Plan","")
            
            bedBath = apartment.find(attrs={"data-label":"Beds"})
            if bedBath:
                bedBath = bedBath.text.strip().replace("Bed/Bath","")
            
            price = apartment.find(attrs={"data-selenium-id":re.compile("Rent.*")})
            if price:
                price = price.text.strip().replace("Rent","").replace("to","").replace("Call for Details","-")
            
            sqft = apartment.find(attrs={"data-label":"Sq.Ft."})
            if sqft:
                sqft = sqft.text.strip().replace("Square Foot","").replace("to","")
            data.loc[data.size] = {"FloorPlan":floorPlan,"BedBath":bedBath, "Price":price, "sqft":sqft}
    
data.dropna(how="all", inplace=True)
data.drop_duplicates(inplace=True)
data.fillna("-", inplace=True)
data.index = np.arange(len(data))

print(data)
# data.to_excel("apartmentPrices.xlsx", "luxeAlewife")
with pd.ExcelWriter('apartmentPrices.xlsx', engine='openpyxl', mode='a', if_sheet_exists="new") as writer:  
    data.to_excel(writer, sheet_name='luxeAlewife')