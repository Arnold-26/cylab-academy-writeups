#!/bin/bash
export SSHPASS=qX7p-yZ0EX
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 17161 academy@chatelaine.cylabacademy.net"
$SSH 'cat .server.py' 2>&1 | tail -25
