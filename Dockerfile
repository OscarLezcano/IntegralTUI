FROM python:3.13-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
COPY src/ ./src/

RUN useradd -m -s /bin/bash integral \
    && mkdir -p /run/sshd \
    && rm -f /etc/ssh/ssh_host_*_key /etc/ssh/ssh_host_*_key.pub \
    && ssh-keygen -q -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N "" \
    && ssh-keygen -q -t rsa -f /etc/ssh/ssh_host_rsa_key -N ""

COPY docker/sshd_config /etc/ssh/sshd_config
COPY docker/run_tui.sh /app/run_tui.sh
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh /app/run_tui.sh

EXPOSE 2222

ENTRYPOINT ["/entrypoint.sh"]
