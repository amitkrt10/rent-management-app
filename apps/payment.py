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
    tenantDict = dict(zip(tenantDf['flatNo'], tenantDf['tenantName']))
    flatList = list(tenantDict.keys())
    paymentDf = read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet7")

    #New Payment Form
    st.markdown("<h3 style='text-align: center;'>Payment Details</h3>", unsafe_allow_html=True)
    with st.form("Payment Details",clear_on_submit=True):
        paymentList = []
        paymentDate = st.date_input("Payment Date")
        flatNo = st.selectbox("Flat No.",flatList)
        amount = st.text_input("Payment Amount")
        mode = st.radio("Payment Mode",["Cash","Online Transfer"])
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
            sh = gc.open('rentApp')
            wks = sh[6]
            wks.set_dataframe(paymentDf,(1,1))
            st.success("₹ "+amount+" received from "+tenantName+" by "+mode)