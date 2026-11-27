#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 70_investigative-reversing-0-mystery
echo "=== binaire ==="
file 70_investigative-reversing-0-mystery | cut -c1-110
echo "=== chaines ==="
strings -n 4 70_investigative-reversing-0-mystery | head -30
echo "=== flag en clair ? ==="
strings 70_investigative-reversing-0-mystery | grep -aoE "(academy|picoCTF)\{[^}]*\}" | head -3
echo "=== image ==="
file 70_investigative-reversing-0-mystery.png
echo "=== LSB rapide (rouge bit0) ==="
python3 - <<'EOF'
import numpy as np
from PIL import Image
p='70_investigative-reversing-0-mystery.png'
a=np.asarray(Image.open(p).convert('RGB'))
print("shape:", a.shape)
for ch,name in ((0,'R'),(1,'G'),(2,'B')):
    bits=(a[:,:,ch]&1).ravel()
    n=(len(bits)//8)*8
    data=np.packbits(bits[:n].reshape(-1,8),axis=1).tobytes()
    import re
    m=re.search(rb"[ -~]{10,}", data)
    print(name, "->", (m.group(0)[:80] if m else "(rien)"))
EOF
