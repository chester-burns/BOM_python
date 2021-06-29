import pandas as pd

def csv2html(csv_file, html_fname):
    read = pd.read_csv(csv_file)
    read.to_html("saves/"+html_fname)