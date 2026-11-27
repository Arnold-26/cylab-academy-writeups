#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
rm -rf t54 && mkdir t54 && cd t54 || exit 1
for i in 1 2 3 4 5; do cp ../54_Item0${i}_cp.bmp Item0${i}.bmp; done
python3 -c "open('flag.txt','w').write('A'*50)"
../54_investigative-reversing-4-mystery 2>&1 | head -3
for i in 1 2 3 4 5; do [ -f Item0${i}_cp.bmp ] && mv Item0${i}_cp.bmp encA0${i}.bmp; done
python3 -c "open('flag.txt','w').write('B'*50)"
../54_investigative-reversing-4-mystery >/dev/null 2>&1
for i in 1 2 3 4 5; do [ -f Item0${i}_cp.bmp ] && mv Item0${i}_cp.bmp encB0${i}.bmp; done
ls -la | head -20
