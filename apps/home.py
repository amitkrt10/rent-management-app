import streamlit as st
def app():
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go
    import appModules as am

    #Current Dues
    duesDf = am.read_gsheet(st.secrets["sheetId"],"Sheet8")
    finaldf = duesDf.dropna()
    displayDf = finaldf[finaldf['paymentDue']>0][['flatNo','tenantName','paymentDue']]
    displayDf.sort_values(by=['paymentDue'], ascending=False, inplace=True)
    totalDue = displayDf['paymentDue'].sum()
    lendf = len(displayDf)
    st.markdown(f"<h3 style='text-align: center;'>Current Dues = {totalDue}</h3>", unsafe_allow_html=True)

    fig = go.Figure(data=[go.Table(
    columnorder = [1,2,3],
    columnwidth = [40,80,60],
    header = dict(
        values = [['<b>Flat No.</b>'],
                    ['<b>Tenant Name</b>'],
                    ['<b>Current Dues</b>']],
        line_color='darkslategray',
        fill_color='royalblue',
        align='center',
        font=dict(color='white', size=16),
        height=40
    ),
    cells=dict(
        values=[displayDf['flatNo'],displayDf['tenantName'],displayDf['paymentDue']],
        line_color='darkslategray',
        fill=dict(color=['paleturquoise', 'white']),
        align=['center', 'left', 'right'],
        font=dict(color='black', size=14),
        height=30)
        )
    ])
    fig.update_layout(width=370, height=(50+((lendf+1)*30)), margin=dict(l=0, r=0, t=0, b=0))
    st.write(fig)

    #Electrictity Usage
    meterDf = am.read_gsheet(st.secrets["sheetId"],"Sheet5")
    meterDf = meterDf[meterDf.columns.drop(list(meterDf.filter(regex='Unnamed')))]
    meterDf.drop(['readingDate'],axis=1,inplace=True)
    maxIndex = meterDf.index.max()
    meterDisplayDf = meterDf[meterDf.index>=maxIndex-1]
    meterDisplayDf.set_index(['readingMonth'],inplace=True)
    meterDisplayDf = meterDisplayDf.T
    meterDfCols = list(meterDisplayDf.columns)
    meterDisplayDf["Units"] = meterDisplayDf[meterDfCols[1]] - meterDisplayDf[meterDfCols[0]]
    meterDisplayDf['Flat No.'] = meterDisplayDf.index
    totalUsage = meterDisplayDf['Units'].sum()
    st.markdown(f"<h3 style='text-align: center;'>Electricity Usage  = {totalUsage} KW</h3>", unsafe_allow_html=True)

    fig = go.Figure(data=[go.Table(
    columnorder = [1,2,3,4],
    columnwidth = [40,50,50,40],
    header = dict(
        values = [['<b>Flat No.</b>'],
                    [f'<b>{meterDfCols[1]}</b>'],
                    [f'<b>{meterDfCols[0]}</b>'],
                    [f'<b>Units</b>']],
        line_color='darkslategray',
        fill_color='royalblue',
        align='center',
        font=dict(color='white', size=16),
        height=40
    ),
    cells=dict(
        values=[meterDisplayDf['Flat No.'],meterDisplayDf[meterDfCols[1]],meterDisplayDf[meterDfCols[0]],meterDisplayDf['Units']],
        line_color='darkslategray',
        fill=dict(color=['paleturquoise', 'white']),
        align=['center', 'right', 'right', 'right'],
        font=dict(color='black', size=14),
        height=30)
        )
    ])
    fig.update_layout(width=370, height=(50+((lendf+1)*30)), margin=dict(l=0, r=0, t=0, b=0))
    st.write(fig)