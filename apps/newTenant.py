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

	#options
	flatDF = read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet10")
	flatList = list(flatDF['flatNo'])
	meterDf = read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet4")
	meterDf = meterDf[meterDf.columns.drop(list(meterDf.filter(regex='Unnamed')))]


	#New Tenant Form
	st.markdown("<h3 style='text-align: center;'>New Tenant Details</h3>", unsafe_allow_html=True)
	with st.form("New Tenant Details",clear_on_submit=True):
		newTenantDetails = []
		tenantDf = read_gsheet("1btdfIIxZYTHpadDRxkKDEhOzh8NnFEUB5ugrWPOMgTs","Sheet1")
		flatNo = st.selectbox("Flat No.",flatList)
		tenantName = st.text_input("Enter Full Name")
		tenantMobile = st.text_input("Enter Mobile Number")
		securityDeposite = st.text_input("Secutity Deposite Amount")
		rentAmt = st.text_input("Enter Rent Amount")
		waterCharge = st.text_input("Enter Water Charge")
		garbageCharge = st.text_input("Enter Garbage Charge")
		otherCharge = st.text_input("Enter Other Charge, if any")
		previousDue = st.text_input("Enter Previous Due, if any")
		meterReading = st.text_input("Initial Electric Meter Reading")
		dateOfOccupancy = st.date_input("Date of Occupancy")
		submitted = st.form_submit_button("Submit")
		if submitted:
			if otherCharge=="":
				otherCharge=0
			if previousDue=="":
				previousDue=0
			newTenantDetails.append(flatNo)
			newTenantDetails.append(tenantName)
			newTenantDetails.append(tenantMobile)
			newTenantDetails.append(securityDeposite)
			newTenantDetails.append(rentAmt)
			newTenantDetails.append(waterCharge)
			newTenantDetails.append(garbageCharge)
			newTenantDetails.append(otherCharge)
			newTenantDetails.append(previousDue)
			newTenantDetails.append(meterReading)		
			newTenantDetails.append(dateOfOccupancy)
			tenantDf.loc[len(tenantDf.index)] = newTenantDetails
			tenantDf.sort_values(by=['flatNo'], inplace=True)
			sh = gc.open('rentApp')
			#Update Active Tenant
			wks = sh[0]
			wks.set_dataframe(tenantDf,(1,1))
			#Add Column to Meter Reading
			meterDf[flatNo]=0
			wks = sh[3]
			wks.set_dataframe(meterDf,(1,1))
			st.success("Details of "+tenantName+" submitted successfully for Flat No. "+flatNo)
