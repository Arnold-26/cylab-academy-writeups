#!/bin/bash
export SSHPASS=qX7p-yZ0EX
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 38498 academy@chatelaine.cylabacademy.net"
$SSH 'id; echo "--- ls -la ---"; ls -la; echo "--- sudo -l ---"; echo qX7p-yZ0EX | sudo -S -l 2>&1 | tail -8; echo "--- scripts py ---"; ls -la /usr/bin/*.py /opt/*.py 2>/dev/null; find / -name "*.py" -maxdepth 3 -newer /etc/hostname 2>/dev/null | head' 2>&1 | tail -35
