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

    #Monthly Collection
    st.markdown("<h3 style='text-align: center;'>Monthly Collection</h3>", unsafe_allow_html=True)
    billDf = am.read_gsheet(st.secrets["sheetId"],"Sheet9")
    billDf['newMonth'] = (pd.to_datetime(billDf['billDate'],format='%Y-%m-%d')).apply(lambda x: x.strftime("%m/%Y"))
    billDf['total'] = billDf.iloc[:, -7:-1].sum(axis=1)
    billGroupBy = billDf.groupby(by=['newMonth'])['total'].sum()
    paymentDf = am.read_gsheet(st.secrets["sheetId"],"Sheet7")
    pivotDf = pd.pivot_table(paymentDf,values='amount',index='paymentMonth',columns=['paymentMode'], aggfunc = np.sum)
    try:
        pivotDf['Total'] = pivotDf['Cash'] + pivotDf['Online Transfer']
    except:
        pivotDf['Cash'] = 0
        pivotDf = pivotDf[['Cash','Online Transfer']]
        pivotDf['Total'] = pivotDf['Cash'] + pivotDf['Online Transfer']
    pivotDf = pd.merge(pivotDf,billGroupBy,left_index=True,right_index=True,how='outer')
    pivotDf['ratio'] = pivotDf['Total']/pivotDf['total']*100
    pivotDf['ratio'] = pivotDf['ratio'].apply(lambda x: f"{int(x)}%")
    
    lendf = len(pivotDf)+1
    viewCols = list(pivotDf.columns)
    dfValues = [list(pivotDf.index.values) + ['<b>Total</b>'],
                    list(pivotDf[viewCols[0]]) + [f'<b>{pivotDf[viewCols[0]].sum()}</b>'],
                    list(pivotDf[viewCols[1]]) + [f'<b>{pivotDf[viewCols[1]].sum()}</b>'],
                    list(pivotDf[viewCols[2]]) + [f'<b>{pivotDf[viewCols[2]].sum()}</b>'],
                    list(pivotDf[viewCols[3]]) + [f'<b>{pivotDf[viewCols[3]].sum()}</b>'],
                    list(pivotDf[viewCols[4]]) + [f'<b>{int(pivotDf[viewCols[2]].sum()/pivotDf[viewCols[3]].sum()*100)}%</b>']]

    fig = go.Figure(data=[go.Table(
    columnorder = [1,2,3,4,5,6],
    columnwidth = [40,28,28,28,28,28],
    header = dict(
        values = [['<b>Month</b>'],
                    ['<b>Cash</b>'],
                    ['<b>Online</b>'],
                    ['<b>Total Collection</b>'],
                    ['<b>Total Billed</b>'],
                    ['<b>Collection %</b>']],
        line_color='darkslategray',
        fill_color='royalblue',
        align='center',
        font=dict(color='white', size=12),
        height=40
    ),
    cells=dict(
        values=dfValues,
        line_color='darkslategray',
        fill=dict(color=['paleturquoise', 'white']),
        align=['center', 'right'],
        font=dict(color='black', size=12),
        height=30)
        )
    ])
    fig.update_layout(width=370, height=(100+((lendf+1)*30)), margin=dict(l=0, r=0, t=50, b=0))
    st.write(fig)

#    viewSelect = st.radio("Select View",['Total Collection','Collection Ratio'])
    # Plot raw data
#    def plot_raw_data():
 #       fig = go.Figure()
  #      if viewSelect == 'Total Collection':
   #         fig.add_trace(go.Scatter(x=pivotDf.index, y=pivotDf['Total'], name="Total Collection"))
    #    if viewSelect == 'Collection Ratio':
     #       fig.add_trace(go.Scatter(x=pivotDf.index, y=pivotDf['ratio'], name="Collection Ratio"))
      #  fig.layout.update(title_text='Monthly Collection', xaxis_rangeslider_visible=True)
       # st.plotly_chart(fig)
    #plot_raw_data()

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
    lendf = len(meterDisplayDf)
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