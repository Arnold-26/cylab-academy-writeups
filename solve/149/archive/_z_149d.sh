#!/bin/bash
cd /tmp/cylab_eps || exit 1
for n in 4 6 8 10 12 16 20 24 32 40 48 64; do
  p=$(python3 -c "print('A'*$n)")
  out=$(timeout 5 ./149_checkpass "$p" 2>&1 | head -2 | tr '\n' ' ')
  echo "len=$n -> $out"
done
