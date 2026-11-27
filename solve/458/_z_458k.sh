#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
P='academy{0n3_bi7_4t_a_7im3}'
echo "=== longueur: ${#P} ==="
printf '%sA\n' "$P" | ./458_perplexed
echo "--- variante avec '!' ---"
printf '%s!\n' "$P" | ./458_perplexed
