'''
#####################  FastAPI + TinyLlama Backend API #########################################
Author: Adrián Baeza Prieto
Github: @adribaeza
Python 3.10+
'''
import logging
import torch
from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from transformers import pipeline
from starlette.middleware.cors import CORSMiddleware #Import the middleware
import json
from pydantic import BaseModel
import asyncio
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Static token for the API
STATIC_TOKEN = os.getenv("SERVICE_TOKEN")

# Verify that the SERVICE_TOKEN is defined in the environment variables
if STATIC_TOKEN is None:
    raise ValueError("The SERVICE_TOKEN environment variable is not defined")

#Default LLM configuration values
DEFAULT_MAX_NEW_TOKENS = 100
DEFAULT_DO_SAMPLE = False
DEFAULT_TEMPERATURE = 0.3
DEFAULT_TOP_K = 50
DEFAULT_TOP_P = 0.6
LLM_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#Set default route for the API with prefix /api/v1
api_router = APIRouter(prefix="/api/v1")

# Instance FastAPI
api = FastAPI(title='LLM Chat Service with TinyLLama', 
              description='LLM Chat Service with TinyLlama by Adrián Baeza Prieto',
              version="1.0.0")

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str):
    if token != STATIC_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    verify_token(token)
    return {"sub": "user"}

# Define configuration for the API
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

logging.info('Adding v1 endpoints..')

# Load the model with the TinyLlama model
pipe = pipeline("text-generation", model=LLM_MODEL, torch_dtype=torch.bfloat16, device_map="auto")

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    max_new_tokens: int = DEFAULT_MAX_NEW_TOKENS
    do_sample: bool = DEFAULT_DO_SAMPLE
    temperature: float = DEFAULT_TEMPERATURE
    top_k: int = DEFAULT_TOP_K
    top_p: float = DEFAULT_TOP_P


# max_new_tokens:   Specifies the maximum number of tokens that the model will generate in the response.
#                   A token can be a word, part of a word, or a punctuation symbol.
# do_sample:    Indicates whether to use sampling instead of always taking the token with the highest probability.
#               If True, the model will select tokens based on a probability distribution,
#               which can generate more varied and creative responses.
# temperature:  Controls the randomness of the model's predictions. A higher value (e.g., 1.0) will make the predictions more diverse,
#               while a lower value (e.g., 0.2) will make the predictions more deterministic and repetitive.
# top_k: Limits the model's predictions to the k most probable tokens. 
#        For example, if top_k=50, the model will only consider the top 50 most probable tokens at each step of generation.
# top_p: Also known as nucleus sampling, this parameter sets a cumulative probability threshold. 
#        For example, if top_p=0.9, the model will consider tokens whose cumulative probability is up to 90%,
#        which can help generate more coherent and less error-prone responses.
def generate_text(prompt, max_new_tokens, do_sample, temperature, top_k, top_p):
    if top_p is not None:
        do_sample = True
    return pipe(
        prompt,
        max_new_tokens=max_new_tokens,
        do_sample=do_sample,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p
    )

async def process_message(messages, max_new_tokens, do_sample, temperature, top_k, top_p):
    # Get prompt from messages
    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    # Model configuration
    loop = asyncio.get_event_loop()
    outputs = await loop.run_in_executor(
        None,
        generate_text,
        prompt,
        max_new_tokens,
        do_sample,
        temperature,
        top_k,
        top_p
    )
    return outputs


# Declare the endpoint for the chat service
@api_router.post("/chat")
async def chat(request: ChatRequest, user: dict = Depends(get_current_user)):
    try:
        logging.info(f"Received request: {request}")
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        outputs = await process_message(
            messages,
            request.max_new_tokens,
            request.do_sample,
            request.temperature,
            request.top_k,
            request.top_p
        )

        #Get the output from the model
        output = outputs[0]["generated_text"]
        assistant_response = output.split("<|assistant|>")[-1].strip()
        json_results = json_results = json.dumps({"response": assistant_response}, ensure_ascii=False, indent=4).encode('utf8')
        return json.loads(json_results)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Include main router in the API
api.include_router(api_router)