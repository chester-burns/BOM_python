import os, json

def get_filepaths(data_req):
    ## Finding appropriate directory for historical data storage
    script_dir = os.path.dirname(__file__)
    script_dir = script_dir.replace('\includes','')

    paths = {}

    req_path = "raw_data/data_"
    full_requests_file_path = os.path.join(script_dir, req_path)
    time = data_req.json()['observations']['data'][0]['local_date_time_full']
    #time = 'TEST'
    paths['req'] = (full_requests_file_path+time+".txt")

    data_fpath = 'csv_files/data.csv'
    paths['data'] = os.path.join(script_dir, data_fpath)

    formatted_data_fpath = 'csv_files/formatted_data.csv'
    paths['fdata'] = os.path.join(script_dir, formatted_data_fpath)

    hist_fpath = 'csv_files/historical_data.csv'
    paths['hist'] = os.path.join(script_dir, hist_fpath)

    formatted_hist_data_fpath = 'csv_files/hist_formatted.csv'
    paths['fhist'] = os.path.join(script_dir, formatted_hist_data_fpath)

    deltas_fpath = 'csv_files/deltas.csv'
    paths['delta'] = os.path.join(script_dir, deltas_fpath)

    return paths