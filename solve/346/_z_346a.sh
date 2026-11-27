#!/bin/bash
cd /tmp/cylab_eps || exit 1
chmod +x 346_game 446_game 2>/dev/null
file 346_game | cut -c1-100
echo "=== strings 346 ==="
strings -n 5 346_game | grep -aviE "glibc|gcc|\.so|gnu|__" | head -15
echo "=== execution 346 (entree vide) ==="
printf '\n' | timeout 5 ./346_game 2>&1 | head -12
echo "=== execution 346 (haut/bas) ==="
printf 'w\n' | timeout 5 ./346_game 2>&1 | head -12
