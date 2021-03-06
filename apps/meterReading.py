import streamlit as st
def app():
    import pandas as pd
    import numpy as np
    import appModules as am
    import dateutil.relativedelta
    import pygsheets
    gc = pygsheets.authorize(service_file='creds.json')

    meterDf = am.read_gsheet(st.secrets["sheetId"],"Sheet3")
    meterDf = meterDf[meterDf.columns.drop(list(meterDf.filter(regex='Unnamed')))]  
    meterCols = list(meterDf.columns)
    flatList = meterCols[2:]
    readingDf = am.read_gsheet(st.secrets["sheetId"],"Sheet4")
    readingDf = readingDf[readingDf.columns.drop(list(readingDf.filter(regex='Unnamed')))]  

    #New Tenant Form
    st.markdown("<h3 style='text-align: center;'>Electric Meter Reading</h3>", unsafe_allow_html=True)
    with st.form("Electric Meter Reading",clear_on_submit=True):
        readingList = []
        readingDfList = []
        readingDate = st.date_input("Reading Date")
        for i in range(len(flatList)):
            tempReading = st.text_input(flatList[i])
            readingList.append(tempReading)
        submitted = st.form_submit_button("Submit")
        if submitted:
            prevMonthDate = readingDate - dateutil.relativedelta.relativedelta(months=1)
            readingDfList.append(readingDate)
            readingDfList.append(str(prevMonthDate.month)+"/"+str(prevMonthDate.year))
            readingDfList = readingDfList + readingList
            readingDf.loc[len(readingDf.index)] = readingDfList
            sh = gc.open(st.secrets["sheetName"])
            wks = sh[3]
            wks.set_dataframe(readingDf,(1,1))
            st.success("Electricity Meter Reading Successfully Submitted")