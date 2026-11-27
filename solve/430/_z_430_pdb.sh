#!/bin/bash
cd /tmp/winadb
echo "=== pdb strings interessantes"
strings -a WinAntiDbg0x300.pdb | grep -iE "academy|flag|config|xor|decrypt|key" | head -25
echo "=== config.bin 0x300 (attention: ecrase par le zip 0x200 ?)"
od -A x -t x1z config.bin | head -8
echo "=== state de l'install"
dpkg -l 2>/dev/null | grep -c ':i386'
pgrep -a dpkg | head -2
pgrep -a apt-get | head -2
