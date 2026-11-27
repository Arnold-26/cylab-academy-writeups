#!/bin/bash
which sshpass || (echo arnold | sudo -S apt-get install -y -qq sshpass 2>&1 | tail -2; which sshpass)
echo "=== test connexion ==="
SSHPASS=e301b3ec sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 30054 ctf-player@chatelaine.cylabacademy.net "echo CONNECTE; ls -la; file flaghasher 2>/dev/null" 2>&1 | tail -15
