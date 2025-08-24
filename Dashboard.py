import streamlit as st
import requests 
import pandas as pd
import matplotlib.pyplot as plt

# Set the API URLs
API_BASE_URL = "http://192.168.178.59:8000/api/"
DASHBOARD_URL = f"{API_BASE_URL}dashboard/1/"
UPLOAD_API_URL = "http://localhost:8000/api/upload-patient-data/"

# Set page configuration
st.set_page_config(page_title="My Health Dashboard", layout="wide")

# Fetch data from the API
response = requests.get(DASHBOARD_URL)
data = response.json()

def upload_csv(file):
    """Function to upload CSV file."""
    try:
        files = {'file': (file.name, file, 'text/csv')}
        response = requests.post(UPLOAD_API_URL, files=files)

        if response.status_code == 201:
            st.success("Data uploaded successfully.")
            st.rerun()  # Refresh the page
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error occurred.')}")
    except Exception as e:
        st.error(f"An exception occurred: {str(e)}")

# Validate the API response
if response.status_code != 200 or 'patient_name' not in data:
    st.error("No patient data available")

    # Title for the upload section
    st.title("Upload Patient Data")
    st.write("Please upload your patient data in CSV format.")

    # File uploader for CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    # Upload button
    if st.button("Upload Data"):
        if uploaded_file is not None:
            upload_csv(uploaded_file)
        else:
            st.warning("Please upload a CSV file.")

else:
    # Convert test results and upcoming appointments to DataFrames
    test_results_df = pd.DataFrame(data['test_results'])
    upcoming_appointments_df = pd.DataFrame(data['upcoming_appointments'])

    # Welcome message with an icon
    st.title(f"Welcome, {data['patient_name']}! 😊")
    st.markdown("---")  # Horizontal line for separation

    # Health alerts section with icons
    st.subheader("Health Alerts ⚠️")
    for alert_data in data['health_alerts_with_recommendations']:
        alert_msg = alert_data['alert']
        st.warning(alert_msg)

        # Links to recommendations pages
        st.page_link("pages/Test_Results.py", label="See Why?")
        st.page_link("pages/Recommendations.py", label="View more recommendations")

    # Display upcoming appointments with an icon
    st.subheader("Upcoming Appointments 📅")
    st.dataframe(upcoming_appointments_df, hide_index=True, use_container_width=True)

    # Prepare test results
    test_results_df['date'] = pd.to_datetime(test_results_df['date'])
    test_results_df['result_numeric'] = test_results_df['result'].replace({'Normal': 1, 'High': 0})

    # Section header for test results
    st.subheader("Test Results 🧪")

    # Display test results with an icon
    st.dataframe(test_results_df, use_container_width=True, hide_index=True)

    st.write("")  # Add a blank line for spacing above the Health Statistics Overview
    st.markdown("<h2 style=' color: #4caf50;'>Health Statistics Overview</h2>",
                unsafe_allow_html=True)

    # Grouping test results by `test_type` and `result`
    result_counts = test_results_df.groupby(['test_type', 'result']).size().unstack(fill_value=0)

    # Define chart types for each test type
    chart_types = {
        'Mammogram': 'bar',
        'Blood Pressure': 'line',
        'Blood Sugar': 'pie',
        'Diabetes': 'pie',
        'Cholesterol': 'bar'
    }

    # Create two columns for chart display
    col1, col2 = st.columns(2)

    # Counter to alternate between columns
    chart_counter = 0

    # Set a fixed height for the charts
    fixed_height = 300  # Height in pixels

    # Map results to numeric values
    result_mapping = {'low': 0, 'Normal': 1, 'High': 2}
    test_results_df['result_value'] = test_results_df['result'].map(result_mapping)
    date_result_df = test_results_df.groupby(['date', 'test_type']).agg({'result_value': 'mean'}).reset_index()

    # Display a variety of charts for different test types
    for test_type in result_counts.index:
        filtered_data = date_result_df[date_result_df['test_type'] == test_type]

        if chart_counter % 2 == 0:
            with col1:
                st.write(f"<h3 style='color: #003366;'>{test_type}</h3>", unsafe_allow_html=True)  # Dark Blue
                st.markdown("<hr>", unsafe_allow_html=True)  # Add horizontal line for separation
                if chart_types[test_type] == 'bar':
                    st.bar_chart(filtered_data.set_index('date')['result_value'], height=fixed_height)
                elif chart_types[test_type] == 'line':
                    st.line_chart(filtered_data.set_index('date')['result_value'], height=fixed_height)
                elif chart_types[test_type] == 'pie':
                    st.write("#### Results Distribution")
                    fig, ax = plt.subplots(figsize=(6, 4))  # Control pie chart size
                    ax.pie(result_counts.loc[test_type], labels=result_counts.columns, autopct='%1.1f%%', startangle=90)
                    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is circular
                    st.pyplot(fig)
        else:
            with col2:
                st.write(f"<h3 style='color: #003366;'>{test_type}</h3>", unsafe_allow_html=True)  # Dark Blue
                st.markdown("<hr>", unsafe_allow_html=True)  # Add horizontal line for separation
                if chart_types[test_type] == 'bar':
                    st.bar_chart(filtered_data.set_index('date')['result_value'], height=fixed_height)
                elif chart_types[test_type] == 'line':
                    st.line_chart(filtered_data.set_index('date')['result_value'], height=fixed_height)
                elif chart_types[test_type] == 'pie':
                    st.write("#### Results Distribution")
                    fig, ax = plt.subplots(figsize=(6, 4))  # Control pie chart size
                    ax.pie(result_counts.loc[test_type], labels=result_counts.columns, autopct='%1.1f%%', startangle=90)
                    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is circular
                    st.pyplot(fig)

        # Increment the counter after each test type
        chart_counter += 1

    # Add space at the end for better readability
    st.write("")

    # Optionally, add a footer or motivational message
    st.markdown(
        "<h3 style='color: #ff7043;'>Stay Informed, Stay Healthy! 🌟</h3>",
        unsafe_allow_html=True
    )

    # Additional CSS for styling
    st.markdown("""
        <style>
            h3 {
                font-size: 24px;
                font-weight: bold;
            }
            h4 {
                font-size: 18px;
                color: #6c757d; /* Gray color for secondary headers */
            }
            .stMarkdown {
                margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)
