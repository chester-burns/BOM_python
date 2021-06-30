import pandas as pd
import csv
from includes.convert import csv2html


def save_data(data, data_file):
    with open(data_file, 'w', newline='') as f:
        ## Writing data headers to current data file 'data.csv'
        writer = csv.writer(f)
        writer.writerow(list(data[0].keys()))

        ## Writing data to current data file 'data.csv'
        for update in data:
            vals = list(update.values())
            for x in range(len(vals)):
                if pd.isnull(vals[x]):
                    vals[x] = 'null'
                    
            writer.writerow(vals)
            
def format_data(data, fdata_file):
    ## Defining parameters for cleaned data, will only contain time and rain data
    cleaned_keys = ['local_date_time_full', 'local_date_time', 'air_temp', 'wind_dir', 'wind_spd_kmh', 'gust_kmh', 'rain_trace']
    cleaned_data = []

    ## Fetching appropriate data based off selection in 'cleaned_keys'
    for i in range(len(data)):
        cleaned_data.append({})
        for k in data[i].keys():
            if k in cleaned_keys:
                cleaned_data[-1][k] = data[i][k]

    ## Writing current formatted data to csv format
    with open(fdata_file,'w', newline='') as fc:
        writer = csv.DictWriter(fc, fieldnames=cleaned_keys)
        writer.writeheader()
        for d in cleaned_data:
            writer.writerow(d)

    return cleaned_keys

def create_historical(fdata_file, hist_file, keys):
    ## Creating a new historical data file

    with open(fdata_file, 'r') as fd:
        with open(hist_file, 'w', newline='') as hd:
            data_reader = list(csv.reader(fd))
            hist_writer = csv.writer(hd)

            hist_writer.writerow(keys)

            initial_data = reversed(data_reader[1:])
            for d in initial_data:
                hist_writer.writerow(d)





def update_historical(fdata_file, hist_file):
    ## Finding any current data that isn't already in historical data
    with open(fdata_file, 'r') as fd:
        with open(hist_file, 'r') as hd:

            current_reader = list(csv.reader(fd))
            hist_reader = list(csv.reader(hd))

            latest_time = int(hist_reader[-1][0])

            new_data_index = 0
            for i in range(len(current_reader[1:])):
                if int(current_reader[i+1][0]) <= latest_time:
                    new_data_index = i-1
                    break
            
            data_to_add = []

            while new_data_index >= 0:
                data_to_add.append(current_reader[1+new_data_index])
                new_data_index -= 1

            #print("Outstanding data from historical file")
            #print(data_to_add)


    ## Writing outstanding data to historical file
    with open(hist_file, 'a+',newline='') as hd:
        writer = csv.writer(hd, delimiter=',')
        for datapoint in data_to_add:
            writer.writerow(datapoint)

    #csv2html(fdata_file, 'formatted.html')

    return len(data_to_add)


def format_historical(hist_file, fhist_file):
    with open(hist_file, 'r') as hd:
        hist_reader = list(csv.reader(hd))
        with open(fhist_file, 'w', newline='') as hf:
            histfm_writer = csv.writer(hf, delimiter=',')
            flipped_hist= reversed(hist_reader[1:])
            
            histfm_writer.writerow(hist_reader[0])

            for line in flipped_hist:
                histfm_writer.writerow(line)


    #csv2html(fhist_file, 'formatted_historical_data.html')
    #formatted_hist_csv = pd.read_csv(fhist_file)
    #formatted_hist_csv.to_html('formatted_historical_data.html')


def delta_calc(fhist_file, deltas_file, pos_only):
    ## Create rain deltas

    ## Calculates rain deltas for ALL historical data
    with open(fhist_file, 'r') as hd:
        reader = list(csv.reader(hd))

        delta_list = []
        for i in range(len(reader[1:-1])):

            curr_data = date = reader[i+1]


            date = curr_data[0][6:8] + "/" + curr_data[0][4:6] + "/" + curr_data[0][0:4]
            time = curr_data[1][-7:]
            temp = curr_data[2]
            wind_direction = curr_data[3]
            wind = float(curr_data[4])/3.6
            gust = float(curr_data[5])/3.6
            rain = curr_data[6]

            delta = float(rain) - float(reader[i+2][6])
            delta_row = [date, time, temp, wind_direction, str(round(wind,2)), str(round(gust,2)), rain, str(round(delta,2))]
            
            if delta <= 0:
                delta_row.append('')
            else:
                delta_row.append('*')
            if pos_only:
                if delta > 0:
                    delta_list.append(delta_row)
            else:
                delta_list.append(delta_row)
            
        #delta_list.append([reader[-1][0][6:8] + "/" + reader[-1][0][4:6] + "/" + reader[-1][0][0:4], reader[-1][1][-7:], reader[-1][2], str(0.0)])


    with open(deltas_file, 'w', newline='') as df:
        writer = csv.writer(df, delimiter=',')
        headings = ['Date', 'Time', 'Air Temp (*C)', 'Wind Direction', 'Wind Speed (m/s)', 'Gust Speed (m/s)', 'Rain since 9am (mm)', 'Rain since last check (mm)', ' ']
        writer.writerow(headings)
        for x in delta_list:
            writer.writerow(x)

    #csv2html(deltas_file, 'rain_data.html')
