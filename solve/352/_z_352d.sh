#!/bin/bash
export SSHPASS=qX7p-yZ0EX
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 17161 academy@chatelaine.cylabacademy.net"
$SSH 'id; echo "--- home ---"; ls -la; echo "--- sudo -l ---"; echo qX7p-yZ0EX | sudo -S -l 2>&1 | tail -8' 2>&1 | tail -30
