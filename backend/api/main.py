'''
#####################  FastAPI + TinyLlama + Docker #########################################
Autor: Adrián Baeza Prieto
Github: @adribaeza
Python 3.10+
'''
import logging
import torch
from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from transformers import pipeline
import docs #Import the documentation
from starlette.middleware.cors import CORSMiddleware #Import the middleware
import json
from pydantic import BaseModel
import asyncio
import os

#instance logger
logger = logging.getLogger(__name__)

#Set default route for the API with prefix /api/v1
api_router = APIRouter(prefix="/api/v1")

# Instance FastAPI
api = FastAPI(title='LLM Chat Service with TinyLLama', description=docs.desc, version=docs.version)

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Static token for the API
STATIC_TOKEN = "myllservicetoken2024"
#STATIC_TOKEN = os.getenv("STATIC_TOKEN")

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
logger.info('Adding v1 endpoints..')

# Load the model with the TinyLlama model
pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")


class ChatRequest(BaseModel):
    text: str


def generate_text(prompt, max_new_tokens, do_sample, temperature, top_k, top_p):
    return pipe(
        prompt,
        max_new_tokens=max_new_tokens,
        do_sample=do_sample,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p
    )

async def process_message(messages):
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
        256,  # max_new_tokens
        True,  # do_sample
        0.5,  # temperature
        50,  # top_k
        0.8  # top_p
    )
    return outputs


# Declare the endpoint for the chat service
@api_router.post("/chat")
async def chat(request: ChatRequest, user: dict = Depends(get_current_user)):
    try:
        #Define the messages to send to the model
        messages = [
            {
                "role": "system",
                "content": "Hi there! How can I help you today?",
            },
            {   
                "role": "user", 
                "content": f"{request.text}"
            },
        ]

        # Process the messages with the model and get the output in async mode
        outputs = await process_message(messages)

        #Get the output from the model
        output = outputs[0]["generated_text"]
        assistant_response = output.split("<|assistant|>")[-1].strip()
        json_results = json_results = json.dumps({"response": assistant_response}, ensure_ascii=False, indent=4).encode('utf8')
        return json.loads(json_results)
    except Exception as e:
        logger.error(f'Error: {e}')
        raise HTTPException(status_code=500, detail='Internal Server Error')

# Include main router in the API
api.include_router(api_router)

# Execute the API with Uvicorn only if the script is executed directly in the local environment
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(api)