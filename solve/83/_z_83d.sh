#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
rm -rf t83 && mkdir t83 && cd t83 || exit 1
cp ../83_investigative-reversing-3-encoded.bmp original.bmp
python3 -c "open('flag.txt','w').write('academy{' + 'A'*42)"
ls -la
chmod +x ../83_investigative-reversing-3-mystery
../83_investigative-reversing-3-mystery 2>&1 | head -5
ls -la
python3 - <<'EOF'
a = open('original.bmp','rb').read()
try:
    b = open('encoded.bmp','rb').read()
except FileNotFoundError:
    print("encoded.bmp absent")
    raise SystemExit
print("tailles:", len(a), len(b))
diffs = [i for i in range(min(len(a), len(b))) if a[i] != b[i]]
print("nb octets differents:", len(diffs))
print("premiers offsets:", diffs[:20])
for i in diffs[:24]:
    print("  %d: %02x -> %02x" % (i, a[i], b[i]))
EOF
