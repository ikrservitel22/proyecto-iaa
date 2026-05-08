FROM ubuntu:22.04

# Evitar prompts
ENV DEBIAN_FRONTEND=noninteractive

# Instalar Python + SSH + herramientas
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    openssh-server \
    sudo \
    git \
    curl \
    && apt clean

# Crear usuario de trabajo
RUN useradd -ms /bin/bash devuser && echo "devuser:devpass" | chpasswd

RUN curl -fsSL https://ollama.com/install.sh | sh

# Dar permisos sudo (opcional)
RUN usermod -aG sudo devuser

# Instalar dependencias Python
RUN pip3 install requests

# Configurar SSH
RUN mkdir /var/run/sshd

# Permitir login por password (solo dev)
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Exponer SSH
EXPOSE 22

# Iniciar SSH
CMD ["/usr/sbin/sshd", "-D"]

WORKDIR /app
COPY main.py .
COPY start.sh .
RUN chmod +x start.sh
