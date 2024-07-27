'''
#####################  FastAPI + TinyLlama + Docker #########################################
Autor: Adrián Baeza Prieto
Github: @adribaeza
Python 3.10+
'''
import logging
import os
import torch
from fastapi import FastAPI, HTTPException
from transformers import pipeline
import docs #Import the documentation
from starlette.middleware.cors import CORSMiddleware #Import the middleware
import json

#instance logger
logger = logging.getLogger(__name__)
# Instance FastAPI
api = FastAPI(title='LLM Chat Service with TinyLLama', description=docs.desc, version=docs.version)
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

# Declare the endpoint for the chat service
@api.post("/chat")
async def chat(text: str):
    try:
        #Define the messages to send to the model
        messages = [
            {
                "role": "system",
                "content": "Solo quiero la respuesta a la pregunta sin repetir la pregunta, por favor.",
            },
            {   
                "role": "user", 
                "content": f"{text}"
            },
        ]
        #Get the prompt from the tokenizer
        prompt = pipe.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        #Model configuration
        outputs = pipe(
            prompt,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.3,
            top_k=50,
            top_p=0.95,
        )
        #Get the output from the model
        output = outputs[0]["generated_text"]
        assistant_response = output.split("<|assistant|>")[-1].strip()
        json_results = json_results = json.dumps({"response": assistant_response}, ensure_ascii=False, indent=4).encode('utf8')
        return json.loads(json_results)
    except Exception as e:
        logger.error(f'Error: {e}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    
# Execute the API with Uvicorn only if the script is executed directly in the local environment
#if __name__ == '__main__':
#    import uvicorn
#    uvicorn.run(api)