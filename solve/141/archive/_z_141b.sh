#!/bin/bash
cd /tmp/cylab_eps/o141 || exit 1
for F in duck.png evil_duck.png; do
  echo "########## $F ##########"
  file "$F"
  python3 - "$F" <<'EOF'
import sys, struct
d = open(sys.argv[1],'rb').read()
print("taille:", len(d), "| debut:", d[:8].hex())
i = d.rfind(b'IEND')
print("IEND a:", i, "| octets apres IEND:", len(d)-(i+8) if i>=0 else "n/a")
if i >= 0 and len(d) > i+8:
    print("data apres IEND:", d[i+8:i+8+100])
# chunks PNG
j = 8
chunks = []
while j+8 <= len(d):
    ln = struct.unpack_from(">I", d, j)[0]
    typ = d[j+4:j+8].decode('latin-1','replace')
    chunks.append((typ, ln))
    j += 12 + ln
    if typ == 'IEND':
        break
print("chunks:", chunks[:15], "..." if len(chunks)>15 else "")
EOF
  echo "--- strings suspectes ---"
  strings -n 8 "$F" | grep -aiE "flag|academy|picoCTF|hidden|map|duck|treasure|next" | head -10
  echo
done
