#!/bin/bash
cd /tmp/cylab_bin || exit 1
python3 - <<'EOF'
import struct
data = open('179_vuln','rb').read()
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
def to_addr(foff):
    for v,o,s in segs:
        if o <= foff < o+s:
            return v + (foff - o)
    return None
# gadgets utiles : pop rdi (5f c3), pop rsi (5e c3), pop rdx (5a c3), ret (c3), pop rdi;pop rbp (5f 5d c3)
pats = {
    'pop rdi; ret': bytes([0x5f, 0xc3]),
    'pop rsi; ret': bytes([0x5e, 0xc3]),
    'pop rdx; ret': bytes([0x5a, 0xc3]),
    'ret': bytes([0xc3]),
    'pop rdi; pop rbp; ret': bytes([0x5f, 0x5d, 0xc3]),
    'pop rax; ret': bytes([0x58, 0xc3]),
}
for name, pat in pats.items():
    hits = []
    start = 0
    while True:
        i = data.find(pat, start)
        if i < 0:
            break
        a = to_addr(i)
        if a:
            hits.append((a, [hex(b) for b in pat]))
        start = i + 1
    print(name, '->', [(hex(a),) for a, _ in hits[:6]])
EOF
