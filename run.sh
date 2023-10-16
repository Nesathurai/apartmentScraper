#! /bin/bash

# cp --backup=t apartmentPrices.xlsx data/apartmentPrices_$(date +%F+%T).xlsx
cp apartmentPrices.xlsx data/apartmentPrices_$(date +%F+%T).xlsx
rm apartmentPrices.xlsx 

# fuseCambridge needs to go first because it creates the excel file 
python3 fuseCambridge.py
python3 hanoverAlewife.py
python3 luxeAlewife.py
python3 hanoverNorth.py
python3 windsorAtCambridge.py