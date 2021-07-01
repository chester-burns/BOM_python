import csv
import pandas as pd
from pretty_html_table import build_table

def export_data(date, delta_file):
    with open('csv_files/export.csv', 'w', newline = '') as e:
        writer = csv.writer(e, delimiter=',')
        with open(delta_file, 'r') as df:
            reader = list(csv.reader(df))
            headings = reader[0]
            headings[-3] = "Total Rain (mm)"
            ttl_rain = 0.0
            writer.writerow(headings[1:])
            for row in reversed(reader):
                if row[0] == date:
                    ttl_rain += float(row[-2])
                    row[-3] = ttl_rain
                    writer.writerow(row[1:])

    df = pd.read_csv('csv_files/export.csv')
    html_table_blue_light = build_table(df, 'red_dark', font_size='large', font_family='Open Sans, sans-serif', index=True)
    title = '<h style = "font-family: Open Sans, sans-serif;font-size: 28;color: #000000;text-align: center;padding: 0px 20px 0px 0px;width: auto"><b>HOLSWORTHY WEATHER OBSERVATIONS - ' + date + '</b></h>'
    
    
    with open('saves/weather_export.html', 'w') as f:
        f.write(title)
        f.write('<p>Total rain column may be different to "rain since 9am" column in historical data as it is calculated from 12AM of the input date</p>')
        f.write(html_table_blue_light)
    