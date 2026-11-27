#!/bin/bash
export SSHPASS='a630e1f8'
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 10075 ctf-player@xebec.cylabacademy.net"
timeout 40 $SSH 'cd ~ && echo "" | timeout 20 ./start 2>&1 | head -60' 2>&1 | tail -70
