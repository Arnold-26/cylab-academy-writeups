#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== calculate_key ==="
objdump -d -Mintel --start-address=0x1261 --stop-address=0x129c 39_need-for-speed 2>/dev/null | tail -20
echo "=== get_key ==="
objdump -d -Mintel --start-address=0x131c --stop-address=0x1355 39_need-for-speed 2>/dev/null | tail -20
echo "=== print_flag ==="
objdump -d -Mintel --start-address=0x1355 --stop-address=0x138b 39_need-for-speed 2>/dev/null | tail -16
