import streamlit as st
import requests

# Set the API URL
DELETE_API_URL = "http://localhost:8000/api/patients/delete/"
UPLOAD_API_URL = "http://localhost:8000/api/upload-patient-data/"

def delete_patient_data():
    try:
        # Construct the complete URL for the delete request
        response = requests.delete(f"{DELETE_API_URL}", headers={"Authorization": "Bearer <your_token>"})

        # Check the response status
        if response.status_code == 204:
            st.success("Patient data deleted successfully.")
        elif response.status_code == 404:
            st.error("Patient not found.")
        else:
            st.error(f"An error occurred: {response.json().get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"An exception occurred: {str(e)}")

def main():
    # Set the page layout and title with styling
    st.set_page_config(page_title="Delete Patient Data", layout="centered")
    st.markdown("<h1 style='font-size: 2.5em; text-align: center;'>🗑️ Delete My Data</h1>", unsafe_allow_html=True)
    st.markdown("---")  # Horizontal line for visual separation

    # Information message with updated background color
    st.markdown(
        "<div style='background-color: #ffecb3; padding: 15px; border-radius: 10px; border: 1px solid #ffc107;'>"
        "<h4 style='color: #ff9800;'>Important:</h4>"
        "<p style='color: #333;'>This action will permanently delete your patient data. Please proceed with caution.</p>"
        "</div>",
        unsafe_allow_html=True
    )

    # Create spacing before the button
    st.write("")  # Add a blank line for spacing
    st.write("")  # Add an extra blank line for more spacing

    # Create a styled button
    if st.button("Delete"):
        delete_patient_data()

    # Optional footer or motivational message
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #ff7043;'>Stay Healthy and Informed! 🌟</h3>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
