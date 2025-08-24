import streamlit as st
import requests 
import pandas as pd

API_BASE_URL = "http://192.168.178.59:8000/api/"
DASHBOARD_URL = f"{API_BASE_URL}dashboard/1/"

st.set_page_config(page_title="My Health Dashboard")

response = requests.get(DASHBOARD_URL)
data = response.json()

# Convert test results to DataFrame for better visualization
test_results_df = pd.DataFrame(data['test_results'])

# Convert upcoming appointments to DataFrame
upcoming_appointments_df = pd.DataFrame(data['upcoming_appointments'])


# Welcome message
st.title(f"Welcome, {data['patient_name']}!")


# Health alerts section with link to recommendations
st.subheader("Health Alerts")
for alert_data in data['health_alerts_with_recommendations']:
    alert_msg = alert_data['alert']
    st.warning(alert_msg)
    
    # Links to other pages (assuming they exist)
    st.page_link("pages/Test_Results.py", label="See Why?")
    st.page_link("pages/Recommendations.py", label="View more recommendations")

# Upcoming appointments in the second column
st.subheader("Upcoming Appointments")
st.dataframe(upcoming_appointments_df, hide_index=True, use_container_width = True)


# Convert date column to datetime and map result to numeric values
test_results_df['date'] = pd.to_datetime(test_results_df['date'])
test_results_df['result_numeric'] = test_results_df['result'].replace({'Normal': 1, 'High': 0})

# Section header for test results
st.subheader("Test Results")

# Test results table
st.dataframe(test_results_df, use_container_width=True, hide_index=True)
st.page_link("pages/Test_Results.py", label="View more results")