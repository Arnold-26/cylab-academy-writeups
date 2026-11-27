#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== fin du test de victoire dans main ==="
objdump -d -Mintel --start-address=0x8049816 --stop-address=0x80498b4 345_game 2>/dev/null | head -40
echo "=== init_map (dimensions) ==="
objdump -d -Mintel --start-address=0x80492b8 --stop-address=0x8049330 345_game 2>/dev/null | head -30
