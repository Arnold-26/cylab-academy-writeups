#!/bin/bash
# 218 - vr-school  (Binary Exploitation, picoMini by redpwn)
# Flag: picoCTF{0nl1ne_d3bat3_sux}
# Write-up: ../../../writeups/binary-exploitation/218-vr-school.md
# Script exact utilise pour produire le flag.
#
cd /tmp/cylab_eps || exit 1
echo "=== 218 file ==="
file 218_chall | cut -c1-120
echo "=== symbols ==="
nm 218_chall 2>/dev/null | head -30
echo "=== strings ==="
strings -n 5 218_chall | grep -vE '^(GCC|GLIBC|__|\.)' | head -25
