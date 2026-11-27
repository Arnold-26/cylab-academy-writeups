#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== move_player complet ==="
objdump -d -Mintel --start-address=0x8049533 --stop-address=0x80496de 446_game 2>/dev/null | head -45
echo "=== init_map ==="
objdump -d -Mintel --start-address=0x8049233 --stop-address=0x8049324 446_game 2>/dev/null | head -35
