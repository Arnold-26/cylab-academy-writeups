#!/bin/bash
cd /tmp/cylab_eps || exit 1
chmod +x 146_heapedit
echo "=== Makefile.share ==="
cat 146_Makefile.share
echo "=== binaire ==="
file 146_heapedit | cut -c1-120
readelf -h 146_heapedit | grep Type
echo "=== libc ==="
strings -a 146_libc.so.6 | grep -E "^GNU C Library|release version" | head -3
echo "=== symboles ==="
nm 146_heapedit 2>/dev/null | grep -E " T " | head -10
echo "=== chaines ==="
strings -n 5 146_heapedit | head -20
echo "=== execution locale (entree vide) ==="
echo "" | timeout 5 ./146_heapedit 2>&1 | head -10
