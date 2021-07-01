import csv
import pandas as pd
import datetime as dt
from pretty_html_table import build_table

def export_data(date1, date2, delta_file, name):
    d1 = dt.date(int(date1[-4:]), int(date1[3:5]), int(date1[0:2]))
    d2 = dt.date(int(date2[-4:]), int(date2[3:5]), int(date2[0:2]))

    numdays = (d2 - d1).days
    print(numdays)
    date = []
    if numdays == 0:
        date.append(date1)
    else:
        for i in range(numdays):
            d = str(d1+dt.timedelta(days=i))
            d_str = str(d)[-2:] + '/' + str(d)[5:7] + '/' + str(d)[:4]
            date.append(d_str)

    with open('csv_files/export.csv', 'w', newline = '') as e:
        writer = csv.writer(e, delimiter=',')
        with open(delta_file, 'r') as df:
            reader = list(csv.reader(df))
            headings = reader[0]
            headings[-3] = "Total Rain (mm)"
            ttl_rain = 0.0

            if numdays == 0:
                writer.writerow(headings[1:])
            else:
                writer.writerow(headings)
            for row in reversed(reader):
                if row[0] in date:
                    ttl_rain += float(row[-2])
                    row[-3] = ttl_rain
                    if numdays == 0:
                        writer.writerow(row[1:])
                    else:
                        writer.writerow(row)

    df = pd.read_csv('csv_files/export.csv')
    html_table_blue_light = build_table(df, 'red_dark', font_size='large', font_family='Open Sans, sans-serif', index=True)
    if len(date) == 1:
        
        title = '<h style = "font-family: Open Sans, sans-serif;font-size: 28;color: #000000;text-align: center;padding: 0px 20px 0px 0px;width: auto"><b>' + name + ' WEATHER OBSERVATIONS FOR ' + date[0] + '</b></h>'
    else:
        title = '<h style = "font-family: Open Sans, sans-serif;font-size: 28;color: #000000;text-align: center;padding: 0px 20px 0px 0px;width: auto"><b>' + name + ' WEATHER OBSERVATIONS FOR ' + date[0] + ' - ' + date[-1] + '</b></h>'
    
    
    with open('saves/weather_export.html', 'w') as f:
        f.write(title)
        f.write('<p>Total rain column may be different to "rain since 9am" column in historical data as it is calculated from 12AM of the input date</p>')
        f.write(html_table_blue_light)
    