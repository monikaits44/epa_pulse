import streamlit as st
import requests

# API Base URL
API_BASE_URL = "http://192.168.178.59:8000/api/"
DASHBOARD_URL = f"{API_BASE_URL}dashboard/1/"

# Fetching data from the API
response = requests.get(DASHBOARD_URL)
data = response.json()

# Set the title of the app with custom styling
st.set_page_config(page_title="Health Alerts and Recommendations", layout="wide")
st.title("🩺 Health Alerts and Recommendations")
st.markdown("---")

# Iterate through the alerts and recommendations
for item in data['health_alerts_with_recommendations']:
    disease = item['disease']
    risk_score = item['risk_score']

    # Create a colored container for each alert
    with st.container():
        # Custom styling for disease alert
        st.markdown(
            f"<div style='background-color: #d1e7dd; padding: 15px; border-radius: 10px; border: 1px solid #198754;'>"
            f"<h3 style='color: #0f5132;'>At Risk: {disease}</h3>"
            f"<h4 style='color: rgb(255, 112, 67);'>Risk Score: {risk_score}/10</h4>"
            f"</div>",
            unsafe_allow_html=True
        )

        # Display recommendations with a stylish background
        st.markdown(
            f"<h4 style='color: #6c757d;'>Preventive Recommendations:</h4>",
            unsafe_allow_html=True
        )

        # List the recommendations
        for recommendation in item["recommendations"]:
            st.markdown(f"- {recommendation['content']}")

        # Closing div for recommendations
        st.markdown("</div>", unsafe_allow_html=True)

        # Add a divider for better visual separation
        st.markdown("---")

# Optionally, add a footer or additional information
st.markdown(
    "<h3 style='color: #ff7043;'>Stay Healthy, Stay Informed! 🌟</h3>",
    unsafe_allow_html=True
)

# Additional styling to enhance overall appearance
st.markdown("""
    <style>
        h3 {
            font-size: 24px;
            font-weight: bold;
        }
        h4 {
            font-size: 18px;
        }
        .stMarkdown {
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)
