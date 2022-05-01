import pandas as pd
import urllib
from urllib.request import urlopen
import ssl

# SSL Verification
ssl._create_default_https_context = ssl._create_unverified_context

# Read gsheets
def read_gsheet(sheetId,sheetName):
    url = f"https://docs.google.com/spreadsheets/d/{sheetId}/gviz/tq?tqx=out:csv&sheet={sheetName}"
    data = pd.read_csv(urllib.request.urlopen(url))
    return data