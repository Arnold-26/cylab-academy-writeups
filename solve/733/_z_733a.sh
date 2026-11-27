#!/bin/bash
which sshpass || echo "pas de sshpass"
export SSHPASS='a630e1f8'
timeout 60 sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 10075 ctf-player@xebec.cylabacademy.net 'ls -la; file * 2>/dev/null | head -10' 2>&1 | tail -25
