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

import includes.data_handling as dh
from includes.filepath import get_filepaths
from includes.popup import popupmsg



## Gets data from BOM, 
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
data_req = requests.get("http://www.bom.gov.au/fwo/IDN60801/IDN60801.95761.json", headers=headers)
data_req.raise_for_status()
data = data_req.json()["observations"]["data"]

# Define filenames
fp = get_filepaths(data_req)


## Store raw data response in historical requests folder 'all_requests'
with open(fp['req'], 'w') as save:
    json.dump(data_req.json(), save)

dh.save_data(data, fp['data'])
dh.format_data(data, fp['fdata'])
new_data = dh.update_historical(fp['fdata'], fp['hist'])
dh.format_historical(fp['hist'], fp['fhist'])
dh.delta_calc(fp['fhist'], fp['delta'], False)


if new_data == 0:
    message = "Files are up to date!"
else:
    message = (str(new_data) + " datapoint(s) successfully added")

#popupmsg(message)


df = pd.read_csv(fp['delta'])
html_table_blue_light = build_table(df, 'blue_light', font_size='large', font_family='Open Sans, sans-serif', index=True)

# Save to html file
with open('saves/rain_data.html', 'w') as f:
    f.write(html_table_blue_light)