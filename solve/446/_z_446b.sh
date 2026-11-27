#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== move_player ==="
objdump -d -Mintel 446_game 2>/dev/null | sed -n '/<move_player>:/,/^$/p' | head -40
echo "=== main (extrait) ==="
objdump -d -Mintel 446_game 2>/dev/null | sed -n '/<main>:/,/^$/p' | head -50
