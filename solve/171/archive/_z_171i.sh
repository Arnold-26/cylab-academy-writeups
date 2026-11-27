#!/bin/bash
cd /tmp || exit 1
echo '861836f13e3d627dfa375bdb8389214e' > md5hash.txt
ls -la /usr/share/wordlists/rockyou.txt 2>/dev/null | head -2
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt md5hash.txt 2>&1 | tail -5
john --show --format=raw-md5 md5hash.txt 2>&1 | head -3
