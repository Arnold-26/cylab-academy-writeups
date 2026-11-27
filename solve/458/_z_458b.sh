#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== symboles ==="
nm 458_perplexed 2>/dev/null | grep -E " T | t " | head -20
echo "=== main ==="
objdump -d -Mintel 458_perplexed 2>/dev/null | sed -n '/<main>:/,/^$/p' | head -80
