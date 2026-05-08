#!/bin/bash

# Arrancar el servidor Ollama en segundo plano
ollama serve &
OLLAMA_PID=$!

# Esperar a que Ollama esté listo
echo "Iniciando Ollama..."
until curl -s http://localhost:11434/api/tags > /dev/null 2>&1; do
    sleep 1
done

echo "Descargando modelo llama3.2:1b (primera vez ~1.3GB)..."
ollama pull llama3.2:1b

echo "Modelo listo. Iniciando chat..."
python3 main.py

# Al salir del chat, detener Ollama
kill $OLLAMA_PID