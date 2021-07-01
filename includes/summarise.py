import datetime as dt
import csv

def format_date(d):
    output = d[6:10]+d[3:5]+d[0:2]
    return output

def format_time(t):
    output = t.replace(':', '').replace('am','')
    if 'pm' in output:
        output = output.replace('pm','')
        output = str(int(output)+1200)
    return output

def rain_summary(query_date, deltas_file):
    # Date will be in format YYYYMMDD
    start_date = dt.date(int(query_date[0:4]), int(query_date[4:6]), int(query_date[6:8]))
    end_date = start_date+dt.timedelta(days=1)

    str_start = str(start_date).replace('-','') + "090000"
    str_end = str(end_date).replace('-','') + "090000"

    print("\n\n---Rain data summary for: 9AM", start_date, "-> 9AM", str(end_date)+'---\n')

    total_rain = 0
    deltas = []

    with open(deltas_file, 'r') as df:
        reader = list(csv.reader(df))
        prev = 2
        for row in reader[1:]:

            if format_date(row[0]) == str_start[0:8] and int(format_time(row[1])) >= 900 and float(row[-2]) > 0:
                s = str(reader[prev][0][:5]+ '  |  '+ reader[prev][1] + " -> " + row[1])
                deltas.append((s, row[-2]))
            
            elif format_date(row[0]) == str_end[0:8] and int(format_time(row[1])) < 900 and float(row[-2]) > 0:
                s = str(reader[prev][0][:5]+'  |  '+reader[prev][1] + " -> " + row[1])
                deltas.append((s, row[-2]))
            
            
            if str(format_date(row[0]) + format_time(row[1])+'00') == str_end:
                total_rain = row[-3]
            prev += 1

    print(' Date  |     Time Period      | Rain (mm)')
    for delta in reversed(deltas):
        print('_______|______________________|_________')
        print(delta[0] + '  |', delta[1])
       
    print("\nTotal:", str(total_rain) + "mm")

    
    

    print('\n\n')


    # Identify data for date
    # Pull rain since 9am at next day 9am for total rain
    # Print all rain deltas

