#!/bin/bash
cd . || exit 1
for s in 1 2 3 4 5 6 7 8; do
  out=$(SEED="$s" timeout 300 python3 _z_136_solve.py selftest "${1:-4096}" 2>&1 | tail -1)
  echo "SEED $s -> $out"
done
