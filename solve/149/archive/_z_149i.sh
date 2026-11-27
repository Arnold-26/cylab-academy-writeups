#!/bin/bash
cd /tmp/cylab_eps || exit 1
rm -rf cg2 && mkdir cg2 && cd cg2 || exit 1
for n in 8 10 11 12 13 14 15 16 20 24 32 40; do
  p=$(python3 -c "print('A'*$n)")
  vals=""
  for r in 1 2 3; do
    v=$(valgrind --tool=cachegrind --cachegrind-out-file=/dev/null ../149_checkpass "$p" 2>&1 | grep -oE "I *refs: *[0-9,]+" | head -1 | tr -dc '0-9')
    vals="$vals $v"
  done
  echo "len=$n ->$vals"
done
