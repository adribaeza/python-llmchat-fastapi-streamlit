import streamlit as st
import requests, logging, os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Default LLM configuration values
DEFAULT_MAX_NEW_TOKENS = 100
DEFAULT_DO_SAMPLE = True
DEFAULT_TEMPERATURE = 0.3
DEFAULT_TOP_K = 50
DEFAULT_TOP_P = 0.6



def main():

    # Configuración de la interfaz
    st.title("Chat with TinnyLLama LLM model")
    st.write("Simple chat interface to interact with TinyLlama LLM model")

    #get token from environment
    token = "myllservicetoken2024" #os.getenv("TINYLLAMA_API_TOKEN")

    # Inicializar el historial de mensajes en el estado de la sesión
    if "messages" not in st.session_state:
        st.session_state.messages = []


    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if "request_in_progress" not in st.session_state:
        st.session_state.request_in_progress = False

    if "input_disabled" not in st.session_state:
        st.session_state.input_disabled = False
    
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

    # Input for the user's message
    user_message = st.chat_input("Type your message:",disabled=st.session_state.input_disabled, key="user_message", on_submit=)

    # Botón para enviar el mensaje
    if user_message:

        st.session_state.messages.append({"role": "user", "content": user_message})
        st.session_state.request_in_progress = True
        st.session_state.input_disabled = True


        headers = {
            "Authorization": f"Bearer {token}"
        }

        data = {
            "text": user_message,
            "max_new_tokens": max_new_tokens,
            "do_sample": do_sample,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p
        }
        
        status_placeholder = st.empty()
        status_placeholder.info(f"Sending: {user_message}")

        with st.spinner("The LLM model is thinking..."):
            response = requests.post("http://localhost:8000/api/v1/chat", headers=headers, json=data)
        
        if response.status_code == 200:
            st.session_state.messages.append({"role": "assistant", "content": response.json().get("response")})
            status_placeholder.success("Response received.")
        else:
            st.write("Error:", response.status_code, response.text)
            status_placeholder.error("Error in response.")
        
        ##clear the user message
        user_message = ""
        st.session_state.request_in_progress = False
        st.session_state.input_disabled = False

    
    # Mostrar el historial de mensajes
    for message in st.session_state.messages:
        if message["role"] == "user":
            chat_message = st.chat_message("user")
         
        else:
            chat_message = st.chat_message("assistant")
        chat_message.write(message["content"])

if __name__ == "__main__":
    main()