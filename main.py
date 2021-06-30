'''
--------- BOM Weather Data Scraper ---------
Company: Tactical Group
Created by Chester Burns
Rev: 0.1
'''
## Importing dependencies
import requests
import json
import pandas as pd
from pretty_html_table import build_table
import sys

import includes.data_handling as dh
from includes.filepath import get_filepaths
from includes.popup import popupmsg

DEV = False
CREATE = False
args = sys.argv

if len(args) > 1:
    if args[1] == '-n':
        print("\n*** NEW STATION INITIALISATION ***\nPlease Confirm\n")
        confirm = ''
        while confirm != 'y' and confirm != 'n':
            confirm = input("Are you sure you want to initiliase a new historical dataset? This will overwrite any existing historical data (y/n): ").lower()
        
        if confirm == 'y':
            CREATE = True
    
    elif args[1] == '-d':
        print("\n**DEVELOPER MODE**\n-TG Output Disabled\n")
        DEV = True
        

## Gets data from BOM, 
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
data_req = requests.get("http://www.bom.gov.au/fwo/IDN60801/IDN60801.95761.json", headers=headers)
data_req.raise_for_status()
data = data_req.json()["observations"]["data"]

#data_req = open('all_requests/data_20210628130000.txt',)
#data = json.load(data_req)['observations']['data']
if DEV: print("Data request code:", data_req.status_code)

# Define filenames
fp = get_filepaths(data_req)

if DEV:
    print("\nFilepaths: ")
    for i in range(len(fp)):
        print("   ", str(fp[list(fp.keys())[i]]))
    print('\n')

## Store raw data response in historical requests folder 'all_requests'
with open(fp['req'], 'w') as save:
    json.dump(data_req.json(), save)

dh.save_data(data, fp['data'])
keys = dh.format_data(data, fp['fdata'])
if CREATE:
    dh.create_historical(fp['fdata'], fp['hist'], keys)
else:
    new_data = dh.update_historical(fp['fdata'], fp['hist'])

dh.format_historical(fp['hist'], fp['fhist'])
dh.delta_calc(fp['fhist'], fp['delta'], False)


if new_data == 0:
    message = "Files are up to date!"
else:
    message = (str(new_data) + " datapoint(s) successfully added")



if DEV:
    if new_data == 0:
        print("Files are up to date")
    else:
        print(str(new_data) + " datapoint(s) successfully added")


#popupmsg(message)


df = pd.read_csv(fp['delta'])
html_table_blue_light = build_table(df, 'blue_light', font_size='large', font_family='Open Sans, sans-serif', index=True)

# Save to html file
with open('saves/rain_data.html', 'w') as f:
    f.write(html_table_blue_light)

if DEV == False:
    with open('C:/Users/ChesterBurns/TG/AU P 220172_JNDC - General/08 Constr/3 Program/2 EOTs/BOM Rainfall records/rain_data.html', 'w') as f:
        f.write(html_table_blue_light)