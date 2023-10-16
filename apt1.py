import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import numpy as np
import regex as re

# service = Service(executable_path='/usr/bin/chromedriver')
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(service=service, options=options)
# driver.quit()

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
# URL = 'https://www.hanoveralewife.com/cambridge/hanover-alewife/conventional/'
URL = 'https://hanovernorthcambridge.securecafe.com/onlineleasing/hanover-north-cambridge/floorplans.aspx?nocache=1'
browser.get(URL)

# time.sleep(10)
browser.save_screenshot("screenshot.png")
soup = BeautifulSoup(browser.page_source,"html.parser")
divs = soup.find_all("div", recursive=True)
print(soup.prettify())
data = pd.DataFrame(columns= ["FloorPlan","BedBath","Price","sqft"])

for div in divs:
    floorplans = div.find_all(id=re.compile("floorplans-.*"))
    for floorplan in floorplans:
        apartments = floorplan.find_all(class_="fp-group-item")
        for apartment in apartments:
            floorPlan = apartment.find(class_="fp-name")
            if floorPlan.string:
                floorPlan = floorPlan.string.strip()
            bedBath = apartment.find(class_="fp-col bed-bath").find(class_="fp-col-text")
            if str(bedBath):
                bedBath = re.sub("\<(.*?)\>", "", str(bedBath).strip())
            price = apartment.find(class_="fp-col rent").find(class_="fp-col-text")
            if price.string:
                price = re.sub("[[:alpha:]\s=\/$,]","",price.string.strip())
            sqft = apartment.find(class_="fp-col sq-feet").find(class_="fp-col-text")
            if sqft.string:
                sqft = sqft.string.strip()
            data.loc[data.size] = {"FloorPlan":floorPlan,"BedBath":bedBath, "Price":price, "sqft":sqft}
    
data.drop_duplicates(inplace=True)
data.index = np.arange(len(data))

print(data)
