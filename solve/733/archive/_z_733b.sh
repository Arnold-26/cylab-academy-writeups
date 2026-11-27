#!/bin/bash
export SSHPASS='a630e1f8'
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 10075 ctf-player@xebec.cylabacademy.net"
timeout 60 $SSH 'cat instructions.txt; echo "=== CodeBank ==="; ls -la CodeBank 2>&1 | head -5' 2>&1 | tail -20
echo "=== copie du binaire ==="
timeout 60 sshpass -e scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P 10075 ctf-player@xebec.cylabacademy.net:./start /tmp/start733 2>&1 | tail -2
ls -la /tmp/start733
