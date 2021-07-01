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
from datetime import datetime

import includes.data_handling as dh
from includes.filepath import get_filepaths
from includes.popup import popupmsg
from includes.cleaning import clean
from includes.summarise import rain_summary
from includes.export import export_data

DEV = False
CREATE = False
SUMMARY = False
EXPORT = False
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

    elif args[1] == '-s':
        if len(args)>2:
            SUMMARY = True
    elif args[1] == '-e':
            if len(args) > 2:
                EXPORT = True
        

## Gets data from BOM
link = ''
with open('link.txt','r') as l:
    link = l.read()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
req_link = "http://www.bom.gov.au/fwo/" + link + ".json"
data_req = requests.get(req_link, headers=headers)
data_req.raise_for_status()
data = data_req.json()["observations"]["data"]

if EXPORT:  
    export_data(args[2],'csv_files/deltas.csv', data[0]['name'].upper())
    quit()      


#data_req = open('all_requests/data_20210628130000.txt',)
#data = json.load(data_req)['observations']['data']
if DEV: print("Data request status code:", data_req.status_code)

# Define filenames
fp = get_filepaths(data_req)


if SUMMARY:
    rain_summary(args[2], fp['delta'])

if DEV:
    print("Data stored in:", str(fp['req'][-23:]))


## Store raw data response in historical requests folder 'raw_data'
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
        print("No new data")
    else:
        print(str(new_data) + " datapoint(s) successfully added")


#popupmsg(message)


df = pd.read_csv(fp['delta'])
html_table_blue_light = build_table(df, 'blue_light', font_size='large', font_family='Open Sans, sans-serif', index=True)
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

title = '<h style = "font-family: Open Sans, sans-serif;font-size: 28;color: #000000;text-align: center;padding: 0px 20px 0px 0px;width: auto"><b>' + data[0]['name'].upper() + ' WEATHER OBSERVATIONS - UPDATED AT ' + current_time + '</b></h>'

# Save to html file
save = 'saves/' + data[0]['name'].replace(' ','_').lower() + "_weather_data.html"

with open(save, 'w') as f:
    f.write(title)
    f.write(html_table_blue_light)
    deleted = clean()
    if DEV: print("Cleaning subroutine detected (and removed)", deleted, "unnecessary raw data files\n")

if DEV == False:
    with open('C:/Users/ChesterBurns/TG/AU P 220172_JNDC - General/08 Constr/3 Program/2 EOTs/BOM Rainfall records/holsworthy_historical_data.html', 'w') as f:
        f.write(title)
        f.write(html_table_blue_light)