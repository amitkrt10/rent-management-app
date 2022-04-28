import streamlit as st
def app():
    import pandas as pd
    import numpy as np
    import urllib
    from urllib.request import urlopen
    import ssl
    import pygsheets
    gc = pygsheets.authorize(service_file='creds.json')

    # SSL Verification
    ssl._create_default_https_context = ssl._create_unverified_context

    # Read Data Function
    def read_gsheet(sheetId,sheetName):
        url = f"https://docs.google.com/spreadsheets/d/{sheetId}/gviz/tq?tqx=out:csv&sheet={sheetName}"
        data = pd.read_csv(urllib.request.urlopen(url))
        return data

    st.markdown("<h3 style='text-align: center;'>Current Dues</h3>", unsafe_allow_html=True)
    duesDf = read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet8")
    finaldf = duesDf.dropna()
    finaldf.rename(columns = {'flatNo':'Flat No','tenantName':'Tenant Name','paymentDue':'Current Dues'}, inplace = True)
    st.table(finaldf[['Flat No','Tenant Name','Current Dues']])
