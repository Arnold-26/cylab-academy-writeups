#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
objdump -d -Mintel 50_seed_spring 2>/dev/null | grep -nE 'call.*(srand|rand|time|scanf|__isoc99|gets)' | head -15
echo "=== autour de srand ==="
objdump -d -Mintel 50_seed_spring 2>/dev/null | sed -n '/srand@plt>$/,$p' | head -5
addr=$(objdump -d -Mintel 50_seed_spring 2>/dev/null | grep -B2 'call.*srand' | head -1 | awk '{print $1}' | tr -d ':')
echo "srand appel a: $addr"
