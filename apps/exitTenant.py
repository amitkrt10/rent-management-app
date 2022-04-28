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

    tenantDf = read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet1")
    flatList = list(tenantDf['flatNo'])
    meterDF = read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet4")
    billDf = read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet9")
    paymentDf = read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet7")

    #New Tenant Form
    st.markdown("<h3 style='text-align: center;'>Exit Tenant</h3>", unsafe_allow_html=True)
    with st.form("Exit Tenant",clear_on_submit=True):
        exitList = []
        exitDf = read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet2")
        flatNo = st.selectbox("Flat No.",flatList)
        finalMeterReading = st.text_input("Final Meter Reading")
        exitDate = st.date_input("Exit Date")
        submitted = st.form_submit_button("Submit")
        if submitted:
            filterDf = tenantDf[tenantDf['flatNo']==flatNo]
            filterDfList = filterDf.loc[:, ~filterDf.columns.isin(['waterCharge','garbageCharge','otherCharge','previousDue','initialMeterReading'])].to_numpy().tolist()
            exitList = filterDfList[0]
            exitList.append(finalMeterReading)
            exitList.append(exitDate)
            tenantName = exitList[1]
            sh = gc.open('rentApp')
            #Delete Column from meter reading
            meterDF.drop([flatNo], axis=1, inplace=True)
            wks = sh[3]
            wks.clear()
            wks.set_dataframe(meterDF,(1,1))
            #Remove from Billings
            index_names = billDf[billDf['flatNo']==flatNo].index
            billDf.drop(index_names, inplace = True)
            wks = sh[8]
            wks.clear()
            wks.set_dataframe(billDf,(1,1))
            #Remove from Payments
            index_names = paymentDf[paymentDf['flatNo']==flatNo].index
            paymentDf.drop(index_names, inplace = True)
            wks = sh[6]
            wks.clear()
            wks.set_dataframe(paymentDf,(1,1))
            #Remove From Active List
            index_names = tenantDf[tenantDf['flatNo']==flatNo].index
            tenantDf.drop(index_names, inplace = True)
            wks = sh[0]
            wks.clear()
            wks.set_dataframe(tenantDf,(1,1))
            #Add to Exit List
            exitDf.loc[len(exitDf.index)] = exitList
            wks = sh[1]
            wks.set_dataframe(exitDf,(1,1))
            st.success(tenantName+" is successfully removed from Flat No. "+flatNo)
