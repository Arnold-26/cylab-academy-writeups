#!/bin/bash
cd /tmp/cylab_eps || exit 1
chmod +x 298_pin_checker
echo "=== file ==="
file 298_pin_checker | cut -c1-100
echo "=== strings interessantes ==="
strings -n 6 298_pin_checker 2>/dev/null | grep -iE 'academy|picoCTF|correct|wrong|pin|flag' | head -20
echo "=== run ==="
echo "12345678" | timeout 10 ./298_pin_checker 2>&1 | head -5
