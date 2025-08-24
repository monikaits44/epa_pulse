import streamlit as st
import requests 

API_BASE_URL = "http://192.168.178.59:8000/api/"
DASHBOARD_URL = f"{API_BASE_URL}dashboard/1/"


response = requests.get(DASHBOARD_URL)
data = response.json()

# Display health alerts and recommendations
for alert in data['health_alerts_with_recommendations']:
    st.subheader(alert['alert'])
    st.write("Recommendations:")
    
    for recommendation in alert['recommendations']:
        st.markdown(f"- {recommendation['content']}")