FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    openssh-server \
    sudo \
    git \
    curl \
    zstd \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash devuser && \
    echo "devuser:1234" | chpasswd && \
    usermod -aG sudo devuser && \
    echo "devuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN curl -fsSL https://ollama.com/install.sh | sh

RUN pip3 install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    requests \
    numpy \
    pandas \
    scikit-learn \
    python-multipart

RUN mkdir /var/run/sshd && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 22 8001

CMD ["/start.sh"]