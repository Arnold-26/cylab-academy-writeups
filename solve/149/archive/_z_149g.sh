#!/bin/bash
cd /tmp/cylab_eps || exit 1
rm -rf cg && mkdir cg && cd cg || exit 1
for n in 1 2 3 4 5 6 7 8 9 10 12 16 20 24 28 32 40 48; do
  p=$(python3 -c "print('A'*$n)")
  out=$(valgrind --tool=cachegrind --cachegrind-out-file=cg.$n.log ../149_checkpass "$p" 2>&1 | grep -E "I *refs" | head -1)
  echo "len=$n $out"
done
