from operator import le
from threading import stack_size
import streamlit as st
def app():
    import pandas as pd
    import numpy as np
    import pygsheets
    import plotly.graph_objects as go
    import appModules as am
    gc = pygsheets.authorize(service_file='creds.json')

    #Current Dues
    tenantDf = am.read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet1")
    billDf = am.read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet9")
    paymentDf = am.read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet7")
    flatList = list(tenantDf['flatNo'])
    flatNo = st.selectbox("Select Flat No",flatList)
    statementDf = pd.DataFrame(columns=["Date","Bills","Payments"])
    tenantName = tenantDf[tenantDf['flatNo']==flatNo]['tenantName'].values[0]
    initialDue = tenantDf[tenantDf['flatNo']==flatNo]['previousDue'].values[0]
    if initialDue!=0:
        statementDf.loc[0] = ['Initial Due',initialDue,0]
    billTempDf = billDf[billDf['flatNo']==flatNo]
    billCols = list(billTempDf.columns)
    billTempDf['total'] = billTempDf[billCols[3]] + billTempDf[billCols[4]] + billTempDf[billCols[5]] + billTempDf[billCols[6]] + billTempDf[billCols[7]]
    paymentTempDf = paymentDf[paymentDf['flatNo']==flatNo]
    joinedDf = pd.merge(billTempDf, paymentTempDf, left_on='billDate', right_on='paymentDate', how='outer')
    for i in range(len(joinedDf)):
        billDate = joinedDf[joinedDf.index==i]['billDate'].values[0]
        billAmt = joinedDf[joinedDf.index==i]['total'].values[0]
        paymentDate = joinedDf[joinedDf.index==i]['paymentDate'].values[0]
        paymentAmt = joinedDf[joinedDf.index==i]['amount'].values[0]
        dfList = [billDate,billAmt,0]
        statementDf.loc[len(statementDf)] = dfList
        dfList = [paymentDate,0,paymentAmt]
        statementDf.loc[len(statementDf)] = dfList
        statementDf.dropna(inplace=True)
        statementDf['Bills'] = statementDf['Bills'].astype(int)
        statementDf['Payments'] = statementDf['Payments'].astype(int)
    statementDf["Temp"] = statementDf['Bills'] - statementDf['Payments']
    statementDf["Dues"] = statementDf['Temp'].cumsum()
    lendf = len(statementDf)+1
    viewCols = list(statementDf.columns)
    dfValues = [list(statementDf[viewCols[0]]) + ['<b>Total</b>'],
                    list(statementDf[viewCols[1]]) + [f'<b>{statementDf[viewCols[1]].sum()}</b>'],
                    list(statementDf[viewCols[2]]) + [f'<b>{statementDf[viewCols[2]].sum()}</b>'],
                    list(statementDf[viewCols[4]]) + [f'<b>{statementDf[viewCols[1]].sum()-statementDf[viewCols[2]].sum()}</b>']]

    fig = go.Figure(data=[go.Table(
    columnorder = [1,2,3,4],
    columnwidth = [60,40,40,40],
    header = dict(
        values = [['<b>Date</b>'],
                    ['<b>Bills</b>'],
                    ['<b>Payments</b>'],
                    ['<b>Dues</b>']],
        line_color='darkslategray',
        fill_color='royalblue',
        align='center',
        font=dict(color='white', size=16),
        height=40
    ),
    cells=dict(
        values=dfValues,
        line_color='darkslategray',
        fill=dict(color=['paleturquoise', 'white']),
        align=['center', 'right', 'right', 'right'],
        font=dict(color='black', size=14),
        height=30)
        )
    ],
    layout=go.Layout(title=go.layout.Title(text=f"<b>{tenantName}</b> | Flat No. : <b>{flatNo}</b>"))
    )
    fig.update_layout(width=370, height=(100+((lendf+1)*30)), margin=dict(l=0, r=0, t=50, b=0))
    st.write(fig)

