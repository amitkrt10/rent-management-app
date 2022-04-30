import streamlit as st
def app():
    import pandas as pd
    import numpy as np
    import appModules as am
    from datetime import date
    import dateutil.relativedelta
    import pygsheets
    gc = pygsheets.authorize(service_file='creds.json')
    
    meterDf = am.read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet4")
    meterMonthList = set(meterDf['forMonth'])
    billDf = am.read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet9")
    billMonthList = set(billDf['billMonth'])
    today = date.today()
    prevMonth = (today - dateutil.relativedelta.relativedelta(months=1)).strftime("%m/%Y")
    prevMonth1 = (today - dateutil.relativedelta.relativedelta(months=2)).strftime("%m/%Y")
    prevMonth2 = (today - dateutil.relativedelta.relativedelta(months=2)).strftime("%m/%Y")

    if st.button("Create Bill for "+prevMonth):
        if prevMonth in billMonthList:
            st.error("Bill already created for "+prevMonth)
        else:
            if prevMonth in meterMonthList:
                dateList = [today,prevMonth]
                tenantDf = am.read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet1")
                dueDf = am.read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet8")
                meterDf = am.read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet6")
                tenantDf.drop(['tenantName','mobile','securityDeposite','previousDue','initialMeterReading','dateOfOcupamcy'], axis = 1, inplace = True)
                tenantDfList = tenantDf.values.tolist()
                for i in range(len(tenantDfList)):
                    meterCost = meterDf[tenantDfList[i][0]].sum()*10
                    paymentDue = int(dueDf[dueDf['flatNo']==tenantDfList[i][0]]["paymentDue"])
                    tempList = dateList + tenantDfList[i]
                    tempList.append(meterCost)
                    tempList.append(paymentDue)
                    billDf.loc[len(billDf.index)+i]= tempList
                sh = gc.open('rentApp')
                wks = sh[8]
                wks.set_dataframe(billDf,(1,1))
                st.success("Bills successfully created for the month of "+prevMonth)
            else:
                st.error("Please take the meter reading for "+prevMonth)

    st.markdown("<h3 style='text-align: center;'>View Bills</h3>", unsafe_allow_html=True)
    viewMonthList = []
    if prevMonth in billMonthList:
        viewMonthList.append(prevMonth)
    if prevMonth1 in billMonthList:
        viewMonthList.append(prevMonth1)
    if prevMonth2 in billMonthList:
        viewMonthList.append(prevMonth2)

    if len(viewMonthList)==0:
        st.error("No bills are available for view")
    else:
        viewmonth = st.radio("Select Month",viewMonthList)
        currBillDf = billDf[billDf['billMonth']==viewmonth]
        flatNoList = list(currBillDf['flatNo'])
        flatNo = st.selectbox("Select Flat No.",flatNoList)
        currBillDf = currBillDf[currBillDf['flatNo']==flatNo]
        viewdf = pd.DataFrame(columns=["Paticular", "Amount"])
        rentAmount = currBillDf['rentAmount'].sum()
        electricityCost = currBillDf['meterCost'].sum()
        waterCost = currBillDf['waterCharge'].sum()
        garbage = currBillDf['garbageCharge'].sum()
        other = currBillDf['otherCharge'].sum()
        previousDue = currBillDf['previousDue'].sum()
        totalCost = rentAmount+electricityCost+waterCost+garbage+other+previousDue
        viewdf.loc[len(viewdf.index)]= ["Rent",rentAmount]
        viewdf.loc[len(viewdf.index)]= ["Electricity",electricityCost]
        if waterCost!=0:
            viewdf.loc[len(viewdf.index)]= ["Water",waterCost]
        viewdf.loc[len(viewdf.index)]= ["Garbage",garbage]
        if other!=0:
            viewdf.loc[len(viewdf.index)]= ["Other",other]
        if previousDue!=0:
            viewdf.loc[len(viewdf.index)]= ["Previous Due",previousDue]
        tenantName = tenantDf[tenantDf['flatNo']==flatNo]['tenantName'].values[0]
        st.write(tenantName)
        st.table(viewdf)
        st.info("Total Rent = "+str(totalCost))