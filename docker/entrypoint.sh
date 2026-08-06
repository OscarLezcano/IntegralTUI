#!/bin/sh
set -e

mkdir -p /run/sshd

if [ -n "$SSH_PASSWORD" ]; then
    echo "integral:$SSH_PASSWORD" | chpasswd
    sed -i 's/^PermitEmptyPasswords .*/PermitEmptyPasswords no/' /etc/ssh/sshd_config
else
    passwd -d integral
fi

: > /app/.env
for var in BASE_URL_INTEGRALFIUNI DEBUG_MODE MAIL PASSWORD; do
    value=$(printenv "$var" || true)
    if [ -n "$value" ]; then
        printf '%s="%s"\n' "$var" "$value" >> /app/.env
    fi
done

exec /usr/sbin/sshd -D -e
