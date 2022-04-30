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
    finaldf.rename(columns = {'flatNo':'Flat No','tenantName':'Tenant Name','paymentDue':'Current Dues'}, inplace = True)
    displayDf = finaldf[finaldf['Current Dues']>0][['Flat No','Tenant Name','Current Dues']]
    displayDf.sort_values(by=['Current Dues'], ascending=False, inplace=True)
    displayDf.reset_index(inplace=True)
    displayDf.drop(['index'],axis=1,inplace=True)
    totalDue = displayDf['Current Dues'].sum()
    lendf = len(displayDf)
    st.markdown(f"<h3 style='text-align: center;'>Current Dues = {totalDue}</h3>", unsafe_allow_html=True)
    st.table(displayDf)

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
        values=[displayDf['Flat No'],displayDf['Tenant Name'],displayDf['Current Dues']],
        line_color='darkslategray',
        fill=dict(color=['paleturquoise', 'white']),
        align=['center', 'left', 'right'],
        font=dict(color='black', size=14),
        height=30)
        )
    ])
    fig.update_layout(width=370, height=(((lendf+1)*30)), margin=dict(l=0, r=0, t=0, b=0))
    st.write(fig)

    #Vacant Flats
    flatsDf = am.read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet10")
    occupiedFlatList = list(finaldf['Flat No'])
    flatList = list(flatsDf['flatNo'])
    vacantFlatList = []
    for x in flatList:
        if x not in occupiedFlatList:
            vacantFlatList.append(x)
    vacantFlatDf = flatsDf[flatsDf['flatNo'].isin(vacantFlatList)]
    vacantFlatDf.rename(columns={'flatNo':'Flat No.','type':'Type'}, inplace = True)
    st.markdown(f"<h3 style='text-align: center;'>Vaccant Flats = {len(vacantFlatDf)}</h3>", unsafe_allow_html=True)
    st.table(vacantFlatDf)
