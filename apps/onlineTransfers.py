from email import header
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
    bankDf = am.read_gsheet(st.secrets["sheetId"],"Sheet12")
    bankDf.fillna(0,inplace=True)
    bankDf["Withdrawal"] = bankDf["Withdrawal"].astype(int)
    bankDf["Deposit"] = bankDf["Deposit"].astype(int)
    totalWithdrawal = bankDf["Withdrawal"].sum()
    totalDeposit = bankDf["Deposit"].sum()
    st.info(f"### Balance = ₹ {totalDeposit-totalWithdrawal}")
    statementDf = bankDf
    statementDf["Temp"] = statementDf['Deposit'] - statementDf['Withdrawal']
    statementDf["Balance"] = statementDf['Temp'].cumsum()
    lendf = len(statementDf)+1
    viewCols = list(statementDf.columns)
    dfValues = [list(statementDf[viewCols[0]]) + ['<b>Total</b>'],
                    list(statementDf[viewCols[3]]) + [f'<b>{totalDeposit}</b>'],
                    list(statementDf[viewCols[2]]) + [f'<b>{totalWithdrawal}</b>'],
                    list(statementDf[viewCols[6]]) + [f'<b>{totalDeposit-totalWithdrawal}</b>'],
                    list(statementDf[viewCols[4]]) + ['<b>---</b>']]

    fig = go.Figure(data=[go.Table(
    columnorder = [1,2,3,4,5],
    columnwidth = [25,25,25,25,80],
    header = dict(
        values = [['<b>Date</b>'],
                    ['<b>Credit</b>'],
                    ['<b>Debit</b>'],
                    ['<b>Balance</b>'],
                    ['<b>Remark</b>']],
        line_color='darkslategray',
        fill_color='royalblue',
        align='center',
        font=dict(color='white', size=12),
        height=40
    ),
    cells=dict(
        values=dfValues,
        line_color='darkslategray',
        fill=dict(color=['paleturquoise', 'white', 'white', 'white', 'white']),
        align=['right', 'right', 'right', 'right', 'left'],
        font=dict(color='black', size=10),
        height=30)
        )
    ]
    #layout=go.Layout(title=go.layout.Title(text=f"<b>{tenantName}</b> | Flat No. : <b>{flatNo}</b>"))
    )
    fig.update_layout(width=370, height=(100+((lendf+1)*30)), margin=dict(l=0, r=0, t=50, b=0))
    st.write(fig)

    st.markdown("<h3 style='text-align: center;'>Filters</h3>", unsafe_allow_html=True)
    dfFilter = st.selectbox("Select Category",['Select','Rent','Travel','Bills'])
    if dfFilter=='Select':
        st.write('Select a category')
    if dfFilter=='Rent':
        statementDf = bankDf[bankDf['Remark'].str.contains('Rent')][['Date','Deposit','Remark']]
        headerCol = 'Income'
    if dfFilter=='Travel':
        statementDf = bankDf[bankDf['Remark'].str.contains('Train')][['Date','Withdrawal','Remark']]
        headerCol = 'Expense'
    if dfFilter=='Bills':
        statementDf = bankDf[bankDf['Remark'].str.contains('Bill')][['Date','Withdrawal','Remark']]
        headerCol = 'Expense'

    if dfFilter!='Select':
        lendf = len(statementDf)+1
        viewCols = list(statementDf.columns)
        dfValues = [list(statementDf[viewCols[0]]) + ['<b>Total</b>'],
                        list(statementDf[viewCols[1]]) + [f'<b>{statementDf[viewCols[1]].sum()}</b>'],
                        list(statementDf[viewCols[2]]) + ['<b>---</b>']]

        fig = go.Figure(data=[go.Table(
        columnorder = [1,2,3],
        columnwidth = [40,40,100],
        header = dict(
            values = [['<b>Date</b>'],
                        [f'<b>{headerCol}</b>'],
                        ['<b>Remark</b>']],
            line_color='darkslategray',
            fill_color='royalblue',
            align='center',
            font=dict(color='white', size=16),
            height=40
        ),
        cells=dict(
            values=dfValues,
            line_color='darkslategray',
            fill=dict(color=['paleturquoise', 'white', 'white']),
            align=['right', 'right', 'left'],
            font=dict(color='black', size=14),
            height=30)
            )
        ]
        #layout=go.Layout(title=go.layout.Title(text=f"<b>{tenantName}</b> | Flat No. : <b>{flatNo}</b>"))
        )
        fig.update_layout(width=370, height=(100+((lendf+1)*30)), margin=dict(l=0, r=0, t=50, b=0))
        st.write(fig)