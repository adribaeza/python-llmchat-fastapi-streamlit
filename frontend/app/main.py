'''
#####################  Streamlit Chat With LLM Model   #########################################
Author: Adrián Baeza Prieto
Github: @adribaeza
Python 3.10+
'''
import streamlit as st
import requests, logging, os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the environment variables from the .env file
load_dotenv()

# Get the API URL from the environment variables
api_url = os.getenv('DOCKER_API_URL') if os.getenv('RUNNING_IN_DOCKER') else os.getenv('LOCAL_API_URL')

# Loggin api_url
logging.info(f"API URL: {api_url}")

# Static token for the API
STATIC_TOKEN = os.getenv("SERVICE_TOKEN")
# Verify that the SERVICE_TOKEN is defined in the environment variables
if STATIC_TOKEN is None:
    raise ValueError("The SERVICE_TOKEN environment variable is not defined")

# Default LLM configuration values
DEFAULT_MAX_NEW_TOKENS = 100
DEFAULT_DO_SAMPLE = True
DEFAULT_TEMPERATURE = 0.5
DEFAULT_TOP_K = 50
DEFAULT_TOP_P = 0.9

# Function to clear the chat history
def clear_chat():
    st.session_state.messages = []

def main():

    # Page configuration
    st.set_page_config(
        page_title="Chat with TinyLlama",
        page_icon=":robot_face:",
        layout="centered",
        initial_sidebar_state="auto",
    )

    # Interface title
    st.title("Chat with TinnyLLama LLM model")
    st.write("Simple chat interface to interact with TinyLlama LLM model")

    # Add a button to clear the chat history
    if st.button("➕ New Chat", help="Click to start a new chat and clear the current conversation history"):
        clear_chat()

    # Additional params with help text to adjust the LLM model behavior
    with st.expander("Config params", expanded=False):
        max_new_tokens = st.number_input(
            "Max New Tokens", 
            value=DEFAULT_MAX_NEW_TOKENS, 
            help="The maximum number of new tokens to generate in the response."
        )
        do_sample = st.checkbox(
            "Do Sample", 
            value=DEFAULT_DO_SAMPLE, 
            help="Whether to use sampling; if unchecked, greedy decoding is used."
        )
        temperature = st.slider(
            "Temperature", 
            min_value=0.0, 
            max_value=1.0, 
            value=DEFAULT_TEMPERATURE, 
            help="The sampling temperature; higher values make the output more random."
        )
        top_k = st.number_input(
            "Top K", 
            value=DEFAULT_TOP_K, 
            help="The number of highest probability vocabulary tokens to keep for top-k-filtering."
        )
        top_p = st.slider(
            "Top P", 
            min_value=0.0, 
            max_value=1.0, 
            value=DEFAULT_TOP_P, 
            help="The cumulative probability of parameter highest probability vocabulary tokens to keep for nucleus sampling."
        )

    # Check if the session state has the messages attribute to initialize it
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Iterate over the messages in the session state to display them in the chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Add a chat input to interact with the assistant
    if prompt := st.chat_input("What is up?"):

        # Add the user message to the chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        headers = {
            "Authorization": f"Bearer {STATIC_TOKEN}",
            "Content-Type": "application/json"
        }
        # Build the data payload for the API request
        conversation_history = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
        data = {
            "messages": conversation_history,
            "max_new_tokens": max_new_tokens,
            "do_sample": do_sample,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p
        }
        logging.info(f"Request data: {data}")

        # Make a request to the API
        try:
            with st.spinner("The assistant is thinking..."):
                response = requests.post(api_url, headers=headers, json=data)
                logging.info(f"Response status code: {response.status_code}")
                logging.info(f"Response content: {response.content}")
            if response.status_code == 200:
                assistant_response = response.json().get("response")
                with st.chat_message("assistant"):
                    st.markdown(assistant_response)
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            else:
                st.error("Error in API request")
                logging.error(f"Error in API request: {response.status_code} - {response.content}")
        except requests.exceptions.RequestException as e:
            st.error("Failed to connect to the API")
            logging.error(f"Failed to connect to the API: {e}")

    # Add a footer with the app information
    st.markdown(
        """
        <style>
        .footer-text {
            position: fixed;
            left: 50%;
            bottom: 0px;
            transform: translateX(-40%);
            z-index: 9999;
            background-color: white;
            padding: 0px;
            border-radius: 0px;
        }
        </style>
        <div class="footer-text">
            <p>Powered by TinyLlama LLM model. © 2023 | Developed by <a href="https://github.com/adribaeza" target="_blank">adribaeza</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Run the main function
if __name__ == "__main__":
    main()
   