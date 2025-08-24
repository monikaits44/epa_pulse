import streamlit as st
import requests

# Set the API URL
API_URL = "http://localhost:8000/api/patients/delete/"

def delete_patient_data(patient_id):
    try:
        # Construct the complete URL for the delete request
        response = requests.delete(f"{API_URL}{patient_id}/", headers={"Authorization": "Bearer <your_token>"})

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
    st.title("Delete Patient Data")

    # Input field for patient ID
    patient_id = st.text_input("Enter Patient ID to delete:", "")

    # Delete button
    if st.button("Delete Patient"):
        if patient_id:
            delete_patient_data(patient_id)
        else:
            st.warning("Please enter a valid Patient ID.")

if __name__ == "__main__":
    main()