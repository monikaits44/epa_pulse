import streamlit as st
import requests 
import pandas as pd
import matplotlib.pyplot as plt

API_BASE_URL = "http://192.168.178.59:8000/api/"
DASHBOARD_URL = f"{API_BASE_URL}dashboard/1/"

response = requests.get(DASHBOARD_URL)
data = response.json()

# Convert test results to DataFrame for better visualization
test_results_df = pd.DataFrame(data['test_results'])

# Title and Patient Info
st.title("My Test Results")

# Convert test results to a DataFrame
test_results_df = pd.DataFrame(data['test_results'])

# Display test results table
st.header("Overview")
st.dataframe(test_results_df, use_container_width=True, hide_index=True)

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

result_mapping = {'low': 0, 'Normal': 1, 'High': 2}

# Add a new column for result_value using the mapping
test_results_df['result_value'] = test_results_df['result'].map(result_mapping)
date_result_df = test_results_df.groupby(['date', 'test_type']).agg({'result_value': 'mean'}).reset_index()


# Display a variety of charts for different test types
for test_type in result_counts.index:

    filtered_data = date_result_df[date_result_df['test_type'] == test_type]
    if chart_counter % 2 == 0:
        with col1:
            st.write(f"### {test_type}")
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
            st.write(f"### {test_type}")
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
