#!/bin/sh
set -e

mkdir -p /run/sshd

if [ -n "$SSH_PASSWORD" ]; then
    echo "integral:$SSH_PASSWORD" | chpasswd
    sed -i 's/^PermitEmptyPasswords .*/PermitEmptyPasswords no/' /etc/ssh/sshd_config
else
    passwd -d integral
fi

exec /usr/sbin/sshd -D -e
