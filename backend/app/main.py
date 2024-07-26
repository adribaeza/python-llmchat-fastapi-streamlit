'''
##################### TinyLlama + FastAPI + Docker #########################################
Autor: Santiago Gonzalez Acevedo 
Twitter: @locoalien
Python 3.11+
'''
#https://medium.com/@santiagosk80/tinyllama-fastapi-docker-microservicios-llm-ff99eb999f04
import logging
import os
import torch
from fastapi import FastAPI, HTTPException
from transformers import pipeline
import docs #Libreria con informacion de la API en Swagger
from starlette.middleware.cors import CORSMiddleware #Seguridad a nivel de CORS
import json

logger = logging.getLogger(__name__)
# Crea una instancia de FastAPI
app = FastAPI(title='LLM Chat Service', description=docs.desc, version=docs.version)
# CORS Configuration (in-case you want to deploy)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
logger.info('Adding v1 endpoints..')

# Carga el modelo y el tokenizador
pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")

# Necesito un enpoint "/chat" que reciba un texto, lo pase por el modelo y devuelva la respuesta
@app.post("/chat")
async def chat(text: str):
    try:
         #Configuracion de comportamiento del modelo
            messages = [
                 {
                    "role": "system",
                    "content": "Solo quiero la respuesta a la pregunta sin repetir la pregunta, por favor.",
                },
                {"role": "user", "content": f"{text}"},
            ]
            #Obtener prompt para el modelo
            prompt = pipe.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            #Configuracion de exactitud del modelo
            outputs = pipe(
                prompt,
                max_new_tokens=256,
                do_sample=True,
                temperature=0.3,
                top_k=50,
                top_p=0.95,
            )
            #Resultado del modelo
            output = outputs[0]["generated_text"]
            # Extraer la parte de la respuesta a partir de "<|assistant|>"
            assistant_response = output.split("<|assistant|>")[-1].strip()
            json_results = json_results = json.dumps({"response": assistant_response}, ensure_ascii=False, indent=4).encode('utf8')
            return json.loads(json_results)
    except Exception as e:
        logger.error(f'Error: {e}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    
# Ejecutar el servidor con uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)