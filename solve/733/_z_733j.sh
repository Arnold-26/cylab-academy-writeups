#!/bin/bash
export SSHPASS='a630e1f8'
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 10075 ctf-player@xebec.cylabacademy.net"
timeout 60 sshpass -e scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P 10075 ./_z_733i.py ctf-player@xebec.cylabacademy.net:/tmp/exp733i.py 2>&1 | tail -1
timeout 150 $SSH 'cd ~ && python3 /tmp/exp733i.py 2>&1 | tail -25' 2>&1 | tail -30
