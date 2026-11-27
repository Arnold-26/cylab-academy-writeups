#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== zone 0x8049660 - 0x8049800 ==="
objdump -d -Mintel --start-address=0x8049660 --stop-address=0x8049800 346_game 2>/dev/null | tail -60
