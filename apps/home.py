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

    #Current Dues
    st.markdown("<h3 style='text-align: center;'>Current Dues</h3>", unsafe_allow_html=True)
    duesDf = read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet8")
    finaldf = duesDf.dropna()
    finaldf.rename(columns = {'flatNo':'Flat No','tenantName':'Tenant Name','paymentDue':'Current Dues'}, inplace = True)
    displayDf = finaldf[finaldf['Current Dues']>0]
    displayDf.sort_values(by=['Current Dues'], ascending=False, inplace=True)
    displayDf.reset_index(inplace=True)
    st.table(displayDf[['Flat No','Tenant Name','Current Dues']])
    totalDue = displayDf['Current Dues'].sum()
    st.info("### Total Dues = "+str(totalDue))

    #Vacant Flats
    st.markdown("<h3 style='text-align: center;'>Vaccant Flats</h3>", unsafe_allow_html=True)
    flatsDf = read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet10")
    occupiedFlatList = list(finaldf['Flat No'])
    flatList = list(flatsDf['flatNo'])
    vacantFlatList = []
    for x in flatList:
        if x not in occupiedFlatList:
            vacantFlatList.append(x)
    vacantFlatDf = flatsDf[flatsDf['flatNo'].isin(vacantFlatList)]
    vacantFlatDf.rename(columns={'flatNo':'Flat No.','type':'Type'})
    st.table(vacantFlatDf)
