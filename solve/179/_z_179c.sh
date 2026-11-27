#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_bin || exit 1
python3 - <<'EOF'
data = open('179_vuln','rb').read()
# le .text commence a 0x400540 environ ; on cherche l'offset fichier
# on va mapper les adresses via readelf
import subprocess, re
out = subprocess.run(['readelf','-SW','179_vuln'], capture_output=True, text=True).stdout
for line in out.splitlines():
    if '.text' in line:
        print(line)
# supposons .text addr 0x400540 file off 0x540 (typique)
# cherchons 5f c3
found = []
for i in range(len(data)-1):
    if data[i] == 0x5f and data[i+1] == 0xc3:
        found.append(i)
print("occurences 5f c3:", len(found), found[:10])
# trouver l'offset fichier de .text
import struct
phoff = struct.unpack_from('<Q', data, 0x20)[0]
phentsize = struct.unpack_from('<H', data, 0x36)[0]
phnum = struct.unpack_from('<H', data, 0x38)[0]
segs = []
for i in range(phnum):
    off = phoff + i*phentsize
    p_type = struct.unpack_from('<I', data, off)[0]
    p_offset = struct.unpack_from('<Q', data, off+8)[0]
    p_vaddr = struct.unpack_from('<Q', data, off+16)[0]
    p_filesz = struct.unpack_from('<Q', data, off+32)[0]
    if p_type == 1:
        segs.append((p_vaddr, p_offset, p_filesz))
print("segments:", [(hex(v), hex(o), hex(s)) for v,o,s in segs])
def to_addr(foff):
    for v,o,s in segs:
        if o <= foff < o+s:
            return v + (foff - o)
    return None
for f in found[:10]:
    print(hex(f), '->', hex(to_addr(f)) if to_addr(f) else None)
EOF
