from fastapi import FastAPI
from transformers import GPT2LMHeadModel, GPT2Tokenizer
# Importa tu modelo aquí

app = FastAPI()

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

@app.post("/predict")
async def predict(text: str):
    inputs = tokenizer.encode(text, return_tensors="pt")
    outputs = model.generate(inputs, max_length=100)
    prediction = tokenizer.decode(outputs[0])
    return {"prediction": prediction}