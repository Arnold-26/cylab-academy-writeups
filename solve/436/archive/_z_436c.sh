#!/bin/bash
export SSHPASS='647e170e'
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -p 48141 ctf-player@xebec.cylabacademy.net"
printf '*\n$_\n*/*\n$-\nexit\n' | timeout 60 $SSH 2>&1 | tail -30
