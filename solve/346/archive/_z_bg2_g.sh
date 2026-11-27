#!/bin/bash
cd /tmp/bg2
# test 1: two stamps in a row: lA d lB d  -> does the first stamp survive?
printf 'lAdlBd' > in1.bin
./_z_bg2 < in1.bin > out1.txt 2>&1
echo "--- test1 tail (last map) ---"
tail -40 out1.txt | cat -A | sed -n '1,40p' | sed 's/\$$//' | head -40
echo "--- rows 0..6 of last map ---"
tail -31 out1.txt | head -8 | cat -A | sed 's/\$$//'
echo
echo "--- test2: lA then 3 w then dump ---"
printf 'lAwww' > in2.bin
./_z_bg2 < in2.bin > out2.txt 2>&1
tail -31 out2.txt | head -8 | cat -A | sed 's/\$$//'
