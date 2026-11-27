#!/bin/bash
cd /tmp/cylab_eps || exit 1
rm -rf t13 && mkdir t13 && cd t13 || exit 1
cp ../13_investigative-reversing-2-encoded.bmp original.bmp
chmod +x ../13_investigative-reversing-2-mystery
python3 -c "open('flag.txt','w').write('A'*50)"
../13_investigative-reversing-2-mystery >/dev/null 2>&1
[ -f encoded.bmp ] && mv encoded.bmp encA.bmp
python3 -c "open('flag.txt','w').write('B'*50)"
../13_investigative-reversing-2-mystery >/dev/null 2>&1
[ -f encoded.bmp ] && mv encoded.bmp encB.bmp
python3 - <<'EOF'
a = open('encA.bmp','rb').read()
b = open('encB.bmp','rb').read()
diffs = [i for i in range(min(len(a), len(b))) if a[i] != b[i]]
print("nb diff:", len(diffs))
print("premiers:", diffs[:20])
print("dernier:", diffs[-1] if diffs else None)
st = set(diffs[i+1]-diffs[i] for i in range(len(diffs)-1))
print("strides:", sorted(st)[:8])
EOF
