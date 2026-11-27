#!/bin/bash
B=./_z_bg2
echo "=== adresses des chaines ==="
strings -a -t x "$B" | grep -E 'flag.txt|You win|Player position'
echo "=== fonctions (nm) ==="
nm "$B" | grep -E ' [Tt] ' | sort
echo "=== move_player ==="
objdump -d --start-address=0x8049474 --stop-address=0x8049549 -M intel "$B"
echo "=== main ==="
objdump -d --start-address=0x8049674 --stop-address=0x8049a80 -M intel "$B" | head -120
