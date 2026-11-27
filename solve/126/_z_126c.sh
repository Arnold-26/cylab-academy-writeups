#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== suite de main ==="
objdump -d -Mintel 126_gauntlet 2>/dev/null | sed -n '/<main>:/,/^$/p' | sed -n '25,70p'
echo "=== chaines ==="
strings -n 5 126_gauntlet | head -25
