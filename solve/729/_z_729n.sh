#!/bin/bash
cd /tmp || exit 1
rm -f md5.txt md5.pot
cat > md5.txt <<'EOF'
admin:5a9a79d9fa477ed163b89088681672c9
ctf-player:7a67ab5872843b22b5e14511867c4e43
EOF
echo "=== john ==="
timeout 600 john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt md5.txt 2>&1 | tail -8
echo "=== resultats ==="
john --show --format=raw-md5 md5.txt 2>&1 | head -10
