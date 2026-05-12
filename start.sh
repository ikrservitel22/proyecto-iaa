#!/bin/bash
set -e

# Arrancar SSH
/usr/sbin/sshd

# Arrancar Ollama en background
ollama serve &

# Esperar a que Ollama esté listo
echo "Esperando Ollama..."
until curl -s http://localhost:11434/api/tags > /dev/null 2>&1; do
    sleep 1
done
echo "Ollama listo"

# Descargar modelo si no existe
ollama pull qwen2.5:7b-instruct

# Arrancar FastAPI desde donde está el código
cd /app/ia
exec uvicorn main:app --host 0.0.0.0 --port 8001