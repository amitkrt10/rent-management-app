from email import message
from tkinter import Button
import streamlit as st
def app():
    import pandas as pd
    import numpy as np
    import pygsheets
    import plotly.graph_objects as go
    import appModules as am
    gc = pygsheets.authorize(service_file='creds.json')

    #Current Dues
    duesDf = am.read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet8")
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

    #if st.button("Send Whatsapp"):
        #msg = Hi, Your Total Rent Due till 
        #am.sendwhatmsg_instantly('phone', alert_msg)
