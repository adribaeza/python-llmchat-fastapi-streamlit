import streamlit as st
import requests, logging, os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
# Static token for the API
STATIC_TOKEN = os.getenv("SERVICE_TOKEN")
# Verify that the SERVICE_TOKEN is defined in the environment variables
if STATIC_TOKEN is None:
    raise ValueError("The SERVICE_TOKEN environment variable is not defined")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Default LLM configuration values
DEFAULT_MAX_NEW_TOKENS = 100
DEFAULT_DO_SAMPLE = True
DEFAULT_TEMPERATURE = 0.5
DEFAULT_TOP_K = 50
DEFAULT_TOP_P = 0.9


# Función para limpiar el historial de mensajes
def clear_chat():
    st.session_state.messages = []

def main():

    # Configuración de la página
    st.set_page_config(
        page_title="Chat with TinyLlama",
        page_icon=":robot_face:",  # Puedes usar un emoji o una URL a un favicon específico
        layout="centered",
        initial_sidebar_state="auto",
    )

    # Configuración de la interfaz
    st.title("Chat with TinnyLLama LLM model")
    st.write("Simple chat interface to interact with TinyLlama LLM model")

    # Añadir un botón para iniciar un nuevo chat
    if st.button("➕ New Chat", help="Click to start a new chat and clear the current conversation history"):
        clear_chat()

    # Additional params with help text
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


    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        headers = {
            "Authorization": f"Bearer {STATIC_TOKEN}",
            "Content-Type": "application/json"
        }
        # Construir el historial de la conversación
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
        try:
            with st.spinner("The assistant is thinking..."):
                response = requests.post("http://host.docker.internal:8000/api/v1/chat", headers=headers, json=data)
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

    # Añadir un footer con el texto deseado
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

if __name__ == "__main__":
    main()

#'''
####  Run the Streamlit app
#To run the Streamlit app, execute the following command in the terminal:
#    
#    ```bash
#    streamlit run frontend/app/main.py
#    ```
#'''
   