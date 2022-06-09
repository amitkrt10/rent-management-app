import streamlit as st
def app():
    import pandas as pd
    import numpy as np
    import appModules as am
    import pygsheets
    gc = pygsheets.authorize(service_file='creds.json')
    
    tenantDf = am.read_gsheet(st.secrets["sheetId"],"Sheet1")
    tenantDict = dict(zip(tenantDf['flatNo'], tenantDf['tenantName']))
    flatList = list(tenantDict.keys())
    paymentDf = am.read_gsheet(st.secrets["sheetId"],"Sheet7")

    #New Payment Form
    st.markdown("<h3 style='text-align: center;'>Payment Details</h3>", unsafe_allow_html=True)
    with st.form("Payment Details",clear_on_submit=True):
        paymentList = []
        paymentDate = st.date_input("Payment Date")
        flatNo = st.selectbox("Flat No.",flatList)
        amount = st.text_input("Payment Amount")
        mode = st.radio("Payment Mode",["Cash","Online Transfer","Adjustment"])
        submitted = st.form_submit_button("Submit")
        if submitted:
            tenantName = tenantDict.get(flatNo)
            paymentList.append(paymentDate)
            paymentList.append(str(paymentDate.month)+"/"+str(paymentDate.year))
            paymentList.append(flatNo)
            paymentList.append(tenantName)
            paymentList.append(amount)
            paymentList.append(mode)
            paymentDf.loc[len(paymentDf.index)] = paymentList
            sh = gc.open(st.secrets["sheetName"])
            wks = sh[6]
            wks.set_dataframe(paymentDf,(1,1))
            st.success("₹ "+amount+" received from "+tenantName+" by "+mode)