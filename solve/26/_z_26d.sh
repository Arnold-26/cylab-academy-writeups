#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
rm -rf sstvout && mkdir sstvout && cd sstvout || exit 1
cp ../26_message.wav .
echo "=== decodage auto ==="
timeout 300 sstv -d 26_message.wav -o auto.png 2>&1 | tail -8
ls -la *.png 2>/dev/null
echo "=== modes explicites ==="
for M in "Scottie 1" "Scottie 2" "Scottie DX" "Martin 1" "Robot 36" "PD 120" "PD 180"; do
  timeout 200 sstv -d 26_message.wav -o "m_$(echo $M | tr ' ' '_').png" --mode "$M" 2>/dev/null
done
ls -la m_*.png 2>/dev/null
