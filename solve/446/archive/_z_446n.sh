#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== solve_round ==="
objdump -d -Mintel --start-address=0x80496de --stop-address=0x8049871 446_game 2>/dev/null | tail -45
echo "=== init_player ==="
objdump -d -Mintel --start-address=0x8049506 --stop-address=0x8049533 446_game 2>/dev/null | tail -15
