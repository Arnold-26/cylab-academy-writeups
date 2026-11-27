#!/bin/bash
export SSHPASS=6313d317
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 28959 ctf-player@xebec.cylabacademy.net"
$SSH 'id; echo "--- ls ---"; ls -la; echo "--- bin ---"; ls -l bin 2>/dev/null; file bin 2>/dev/null; echo "--- run ---"; ./bin 2>&1 | head -20; echo "--- strings ---"; strings bin 2>/dev/null | grep -iE "ls|sh|flag|usr/bin|system|PATH" | head -20' 2>&1 | tail -45
