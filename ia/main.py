from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import os
from datetime import datetime

app = FastAPI()

# ─────────────────────────────
# CONFIG
# ─────────────────────────────

with open("config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

OLLAMA_URL = CONFIG["ollama_url"]
MODEL = CONFIG["modelo"]
TEMPERATURE = CONFIG["temperatura"]
MAX_TOKENS = CONFIG["max_tokens"]
NOMBRE = CONFIG["nombre"]
PERSONALIDAD = CONFIG["personalidad"]

MEMORY_FILE = "memory.json"

# ─────────────────────────────
# MODELO REQUEST
# ─────────────────────────────

class ChatRequest(BaseModel):
    message: str

# ─────────────────────────────
# MEMORIA (LEER Y GUARDAR)
# ─────────────────────────────

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def add_memory(user, assistant):
    memory = load_memory()

    memory.append({
        "user": user,
        "assistant": assistant,
        "time": datetime.utcnow().isoformat()
    })

    # opcional: limitar memoria (evita crecer infinito)
    memory = memory[-50:]

    save_memory(memory)

# ─────────────────────────────
# IA CALL CON MEMORIA
# ─────────────────────────────

def call_ollama(message: str):

    memory = load_memory()

    # convertir memoria en contexto corto
    historial = ""
    for item in memory[-10:]:  # solo últimos 10
        historial += f"Usuario: {item['user']}\nIA: {item['assistant']}\n\n"

    prompt_final = f"""
{PERSONALIDAD}

HISTORIAL:
{historial}

USUARIO:
{message}
"""

    payload = {
        "model": MODEL,
        "prompt": prompt_final,
        "stream": False,
        "options": {
            "temperature": TEMPERATURE,
            "num_predict": MAX_TOKENS
        }
    }

    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json=payload,
        timeout=600
    )

    r.raise_for_status()
    return r.json()["response"]

# ─────────────────────────────
# API TEST
# ─────────────────────────────

def call_api_test():
    r = requests.get("http://laravel_web:80/api/test")
    return r.json()

# ─────────────────────────────
# CHAT ENDPOINT
# ─────────────────────────────

@app.post("/chat")
def chat(req: ChatRequest):

    if "api/test" in req.message.lower():
        return call_api_test()

    try:
        respuesta = call_ollama(req.message)
    except Exception as e:
        return {"error": "ollama fallo", "detail": str(e)}

    # guardar memoria (🔥 AQUÍ “aprende”)
    add_memory(req.message, respuesta)

    try:
        return json.loads(respuesta)
    except:
        return {
            "resumen": respuesta,
            "sentimiento_general": "desconocido",
            "temas_principales": [],
            "calidad": 0,
            "riesgos": []
        }

# ─────────────────────────────
# HEALTH
# ─────────────────────────────

@app.get("/")
def home():
    return {
        "status": "ok",
        "model": MODEL,
        "memory_size": len(load_memory())
    }