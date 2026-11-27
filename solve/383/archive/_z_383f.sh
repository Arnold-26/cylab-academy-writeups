#!/bin/bash
cd /tmp/cylab_eps || exit 1
OFF=731136
echo "=== arborescence home/yone ==="
fls -o $OFF -r -p 383_disk.img 2>/dev/null | grep -E "home/yone" | head -40
