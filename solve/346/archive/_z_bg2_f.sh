#!/bin/bash
B=/tmp/bg2/_z_bg2
for f in sigint_handler init_map find_player_pos find_end_tile_pos print_map clear_screen win; do
echo "=== $f ==="
objdump -d -M intel "$B" | sed -n "/<$f>:/,/^\$/p"
done
echo "=== rodata strings ==="
strings -a -t x "$B" | sed -n '1,80p'
