#!/bin/bash
# 318 - Wizardlike  (Reverse Engineering, picoCTF 2022)
# Flag: academy{ur_4_w1z4rd_e14455ad}
# Write-up: ../../../writeups/reverse-engineering/318-wizardlike.md
# This is the script that produced the flag; historical variants are in archive/.
#
cd /tmp/cylab_eps || exit 1
echo "=== file 318 ==="
file 318_game | cut -c1-110
echo "=== strings flag 318 ==="
strings -n 6 318_game | grep -iE 'academy|picoCTF|flag' | head -10
echo "=== 151 instance ==="
