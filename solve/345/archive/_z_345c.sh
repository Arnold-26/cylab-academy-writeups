#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== print_flag_status ==="
objdump -d -Mintel --start-address=0x8049444 --stop-address=0x804947a 345_game 2>/dev/null | tail -15
echo "=== main (debut) ==="
objdump -d -Mintel --start-address=0x8049754 --stop-address=0x8049820 345_game 2>/dev/null | tail -35
