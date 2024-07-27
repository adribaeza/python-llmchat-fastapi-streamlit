import streamlit as st
import requests, logging, os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Default LLM configuration values
DEFAULT_MAX_NEW_TOKENS = 100
DEFAULT_DO_SAMPLE = True
DEFAULT_TEMPERATURE = 0.5
DEFAULT_TOP_K = 50
DEFAULT_TOP_P = 0.9

DEFAULT_TOKEN = "myllservicetoken2024" #os.getenv("TINYLLAMA_API_TOKEN")


def main():

    # Configuración de la interfaz
    st.title("Chat with TinnyLLama LLM model")
    st.write("Simple chat interface to interact with TinyLlama LLM model")

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
            "Authorization": f"Bearer {DEFAULT_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "text": prompt,
            "max_new_tokens": max_new_tokens,
            "do_sample": do_sample,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p
        }
        logging.info(f"Request data: {data}")
        try:
            logging.info("Sending request to API")
            response = requests.post("http://127.0.0.1:8000/api/v1/chat", headers=headers, json=data) #http://localhost:8000
            if response.status_code == 200:
                assistant_response = response.json().get("response", "")
                with st.chat_message("assistant"):
                    st.markdown(assistant_response)
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            else:
                st.error("Error in API request")
        except requests.exceptions.RequestException as e:
            st.error(f"Error en la solicitud: {e}")


if __name__ == "__main__":
    main()