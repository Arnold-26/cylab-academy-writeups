#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== file 318 ==="
file 318_game | cut -c1-110
echo "=== strings flag 318 ==="
strings -n 6 318_game | grep -iE 'academy|picoCTF|flag' | head -10
echo "=== 151 instance ==="
