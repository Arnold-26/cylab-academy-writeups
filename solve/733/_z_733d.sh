#!/bin/bash
export SSHPASS='a630e1f8'
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 10075 ctf-player@xebec.cylabacademy.net"
timeout 60 $SSH 'cd ~ && ./start > /tmp/s.log 2>&1; cat /tmp/s.log; F=$(ls *.c 2>/dev/null | head -1); echo "=== SOURCE: $F ==="; cat "$F"' 2>&1 | tail -80
