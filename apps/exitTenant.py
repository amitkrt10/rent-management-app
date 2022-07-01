import streamlit as st
def app():
    import pandas as pd
    import numpy as np
    import appModules as am
    import pygsheets
    gc = pygsheets.authorize(service_file='creds.json')

    tenantDf = am.read_gsheet(st.secrets["sheetId"],"Sheet1")
    flatList = list(tenantDf['flatNo'])
    meterDF = am.read_gsheet(st.secrets["sheetId"],"Sheet4")
    billDf = am.read_gsheet(st.secrets["sheetId"],"Sheet9")
    paymentDf = am.read_gsheet(st.secrets["sheetId"],"Sheet7")
    exitBillDf = am.read_gsheet(st.secrets["sheetId"],"Sheet13")
    exitPaymentDf = am.read_gsheet(st.secrets["sheetId"],"Sheet14")
    exitDuesDf = am.read_gsheet(st.secrets["sheetId"],"Sheet15")

    #New Tenant Form
    st.markdown("<h3 style='text-align: center;'>Exit Tenant</h3>", unsafe_allow_html=True)
    with st.form("Exit Tenant",clear_on_submit=True):
        exitList = []
        exitDf = am.read_gsheet(st.secrets["sheetId"],"Sheet2")
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
            sh = gc.open(st.secrets["sheetName"])
            # Delete Column from meter reading
            meterDF.drop([flatNo], axis=1, inplace=True)
            wks = sh[3]
            wks.clear()
            wks.set_dataframe(meterDF,(1,1))
            st.write("* Meter Reading Deleted")
            # Add to Exit Dues
            exitDueRecords = billDf[billDf['flatNo']==flatNo]
            exitDuesDf = pd.concat([exitDuesDf,exitDueRecords]).reset_index(drop=True)
            wks = sh[14]
            wks.set_dataframe(exitDuesDf,(1,1))
            st.write("* Dues Copied to Exit Table")
            # Add to Exit Billings
            exitBillRecords = billDf[billDf['flatNo']==flatNo]
            exitBillRecords["tenantName"] == tenantName
            exitBillDf = pd.concat([exitBillDf,exitBillRecords]).reset_index(drop=True)
            wks = sh[12]
            wks.set_dataframe(exitBillDf,(1,1))
            st.write("* Bills Copied to Exit Table")
            # Remove from Billings
            index_names = billDf[billDf['flatNo']==flatNo].index
            billDf.drop(index_names, inplace = True)
            wks = sh[8]
            wks.clear()
            wks.set_dataframe(billDf,(1,1))
            st.write("* Bills Deleted")
            # Add Exit Payments
            exitPaymentRecords = paymentDf[paymentDf['flatNo']==flatNo]
            exitPaymentRecords["tenantName"] = tenantName
            exitPaymentDf = pd.concat([exitPaymentDf,exitPaymentRecords]).reset_index(drop=True)
            wks = sh[13]
            wks.set_dataframe(exitPaymentDf,(1,1))
            st.write("* Payments Copied to Exit Table")
            # Remove from Payments
            index_names = paymentDf[paymentDf['flatNo']==flatNo].index
            paymentDf.drop(index_names, inplace = True)
            wks = sh[6]
            wks.clear()
            wks.set_dataframe(paymentDf,(1,1))
            st.write("* Payments Removed")
            # Remove From Active List
            index_names = tenantDf[tenantDf['flatNo']==flatNo].index
            tenantDf.drop(index_names, inplace = True)
            wks = sh[0]
            wks.clear()
            wks.set_dataframe(tenantDf,(1,1))
            # Add to Exit List
            exitDf.loc[len(exitDf.index)] = exitList
            wks = sh[1]
            wks.set_dataframe(exitDf,(1,1))
            st.success(tenantName+" is successfully removed from Flat No. "+flatNo)
