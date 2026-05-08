from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

app = FastAPI()

CONFIG = {
    "modelo": "qwen3.5:9b",
    "ollama_url": "http://localhost:11434",
    "temperatura": 0.5,
    "max_tokens": 200,
}

# ─────────────────────────────────────────────
# Request body
# ─────────────────────────────────────────────

class ChatRequest(BaseModel):
    mensaje: str
    historial: list = []

# ─────────────────────────────────────────────
# Generar respuesta IA
# ─────────────────────────────────────────────

def generar_respuesta(mensaje, historial):

    system = "Eres un asistente útil que responde en español."

    prompt = system + "\n\n"

    for msg in historial:
        prompt += f"{msg['role']}: {msg['content']}\n"

    prompt += f"user: {mensaje}\nassistant: "

    payload = {
        "model": CONFIG["modelo"],
        "prompt": prompt,
        "stream": False,
        "keep_alive": "30m",
        "options": {
            "temperature": CONFIG["temperatura"],
            "num_predict": CONFIG["max_tokens"],
            "num_ctx": 1024,
        }
    }

    r = requests.post(
        f"{CONFIG['ollama_url']}/api/generate",
        json=payload,
        timeout=120
    )

    r.raise_for_status()

    data = r.json()

    return data["response"]

# ─────────────────────────────────────────────
# Endpoint
# ─────────────────────────────────────────────

@app.post("/chat")
def chat(req: ChatRequest):

    respuesta = generar_respuesta(
        req.mensaje,
        req.historial
    )

    return {
        "respuesta": respuesta
    }