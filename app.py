import streamlit as st
from multiapp import MultiApp
from apps import home, newTenant, exitTenant, meterReading, billing, payment # import your app modules here

# Configure app display
st.set_page_config(
    page_title="Kartikey Bhawan",
    #page_icon="https://pharmeasy.in/favicon.ico",
    #layout="centered",
    layout="wide",
    initial_sidebar_state='collapsed'
)

st.markdown("<h1 style='text-align: center; color: Green;'>Kartikey Bhawan</h1>", unsafe_allow_html=True)

app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Add Tenant", newTenant.app)
app.add_app("Electric Meter Reading", meterReading.app)
app.add_app("Create and Send Bills", billing.app)
app.add_app("Payment Received", payment.app)
app.add_app("Remove Tenant", exitTenant.app)

# The main app
app.run()