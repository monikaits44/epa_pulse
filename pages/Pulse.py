import streamlit as st
import requests
import json

# Set up the page
st.set_page_config(page_title="Pulse", layout="centered")

# Title with reduced size and emoji
st.markdown("<h1 style='font-size: 2.5em; text-align: center;'>💓 Pulse: Your Digital Health Companion</h1>",
            unsafe_allow_html=True)
st.markdown("---")

# Initialize the conversation history in session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Define the new API endpoint
api_endpoint = "http://192.168.178.59:8000/api/medical-bot/"


# Function to send and receive messages in the specified request-response format
def get_response(question):
    try:
        # Prepare the request payload
        payload = {"question": question}

        # Make the request to the API
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            api_endpoint,
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()

        # Parse JSON response
        result = response.json()
        return result.get("response", "Sorry, I didn't understand that.")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


# Display conversation history with custom styling
st.markdown("<h2 style='color: #003366;'>Conversation History</h2>",
            unsafe_allow_html=True)  # Consistent color for subheading
for sender, message in st.session_state.conversation:
    if sender == "You":
        st.markdown(
            f"<div style='margin: 10px 0; background-color: #e1f5fe; padding: 10px; border-radius: 10px; border: 1px solid #81d4fa;'>"
            f"<strong>You:</strong> {message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div style='margin: 10px 0; background-color: #f0f4c3; padding: 10px; border-radius: 10px; border: 1px solid #cddc39;'>"
            f"<strong>Pulse:</strong> {message}</div>", unsafe_allow_html=True)

# Create a sticky container for the input form at the bottom
with st.container():
    # Place the input form at the bottom of the screen
    st.write("")  # Adding empty space for better layout
    with st.form(key="chat_form", clear_on_submit=True):
        user_message = st.text_input("You:", placeholder="Type your message here...")  # Input field for user message
        submit_button = st.form_submit_button(label="Send")

    # Handle message submission
    if submit_button and user_message:
        # Append user message to the conversation history
        st.session_state.conversation.append(("You", user_message))

        # Get response from the API
        response = get_response(user_message)

        # Append chatbot response to the conversation history
        st.session_state.conversation.append(("Pulse", response))

        # Rerun the script to display the new message
        st.rerun()

# Optional footer or motivational message
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #ff7043;'>Stay Healthy and Informed! 🌟</h3>", unsafe_allow_html=True)
