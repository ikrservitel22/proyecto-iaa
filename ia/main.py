from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

app = FastAPI()

# ─────────────────────────────
# CONFIG
# ─────────────────────────────

OLLAMA_URL = "http://localhost:11434"
MODEL = "qwen2.5:7b-instruct"

# ─────────────────────────────
# REQUEST BODY
# ─────────────────────────────

class ChatRequest(BaseModel):
    message: str

# ─────────────────────────────
# IA CALL
# ─────────────────────────────

def call_ollama(message: str):
    payload = {
        "model": MODEL,
        "prompt": message,
        "stream": False
    }

    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json=payload,
        timeout=120
    )

    r.raise_for_status()
    return r.json()["response"]

def call_api_test():
    r = requests.get("http://laravel_web:80/api/test")
    return r.json()

# ─────────────────────────────
# ENDPOINT PRINCIPAL
# ─────────────────────────────

@app.post("/chat")
def chat(req: ChatRequest):

    message = req.message.lower()

    # TOOL: api/test
    if "api/test" in message:
        resultado = call_api_test()

        return {
            "response": f"Resultado API: {resultado}"
        }

    # IA normal
    respuesta = call_ollama(req.message)

    return {
        "response": respuesta
    }

# ─────────────────────────────
# HEALTH CHECK
# ─────────────────────────────

@app.get("/")
def home():
    return {
        "status": "ok",
        "model": MODEL
    }