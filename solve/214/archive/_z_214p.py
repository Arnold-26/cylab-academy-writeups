import sys, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BIN = "/tmp/cylab_eps/214_horse"
d = open(BIN, "rb").read()
phoff = struct.unpack_from("<Q", d, 0x20)[0]
phentsize = struct.unpack_from("<H", d, 0x36)[0]
phnum = struct.unpack_from("<H", d, 0x38)[0]
segs = []
for i in range(phnum):
    off = phoff + i * phentsize
    if struct.unpack_from("<I", d, off)[0] == 1:
        segs.append((struct.unpack_from("<Q", d, off + 16)[0],
                     struct.unpack_from("<Q", d, off + 8)[0],
                     struct.unpack_from("<Q", d, off + 32)[0]))


def off_of(va):
    for v, o, s in segs:
        if v <= va < v + s:
            return o + (va - v)
    return None


for va, name, expect in ((0x400c03, "pop rdi; ret", b"\x5f\xc3"),
                         (0x400c01, "pop rsi; pop r15; ret", b"\x5e\x41\x5f\xc3"),
                         (0x400828, "pop rbp; ret", b"\x5d\xc3"),
                         (0x400b96, "leave; ret", b"\xc9\xc3")):
    o = off_of(va)
    b = d[o:o + len(expect)]
    print(f"{hex(va)} {name:24} bytes={b.hex()} attendu={expect.hex()} {'OK' if b == expect else 'MISMATCH'}")
