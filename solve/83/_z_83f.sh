#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
rm -rf t83b && mkdir t83b && cd t83b || exit 1
cp ../83_investigative-reversing-3-encoded.bmp original.bmp
python3 -c "open('flag.txt','w').write('A'*50)"
cp original.bmp orig_keep.bmp
../83_investigative-reversing-3-mystery >/dev/null 2>&1
mv encoded.bmp encA.bmp
python3 -c "open('flag.txt','w').write('B'*50)"
../83_investigative-reversing-3-mystery >/dev/null 2>&1
mv encoded.bmp encB.bmp
python3 - <<'EOF'
a = open('encA.bmp','rb').read()
b = open('encB.bmp','rb').read()
diffs = [i for i in range(min(len(a), len(b))) if a[i] != b[i]]
print("nb octets differents A vs B:", len(diffs))
print("premiers:", diffs[:30])
print("dernier:", diffs[-1] if diffs else None)
# est-ce contigu ?
if diffs:
    print("contigu de", diffs[0], "a", diffs[-1], ":", len(diffs) == diffs[-1] - diffs[0] + 1)
    # stride
    strides = set(diffs[i+1]-diffs[i] for i in range(len(diffs)-1))
    print("strides observes:", sorted(strides)[:10])
EOF
