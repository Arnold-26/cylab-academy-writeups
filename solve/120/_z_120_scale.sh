#!/bin/bash
cd /tmp
for b in 24 30 32 34; do
  echo "=== dp_bits=$b"
  timeout 900 python3 _z_120_toy.py "$b" 2>&1 | head -6
done
