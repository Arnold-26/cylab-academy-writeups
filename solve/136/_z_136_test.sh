#!/bin/bash
cd . || exit 1
for s in 1 2 3 4 5; do
  echo "=== SEED $s ==="
  SEED="$s" timeout 300 python3 _z_136_crack.py selftest "${1:-4096}" 2>&1 | tail -5
done
