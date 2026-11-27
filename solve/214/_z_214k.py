import sys, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BIN = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/214_horse"
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


def to_addr(fo):
    for v, o, s in segs:
        if o <= fo < o + s:
            return v + (fo - o)
    return None


pats = {
    "pop rbp; ret": b"\x5d\xc3",
    "pop rbp; pop rXX; ret": b"\x5d\x41",
    "leave; ret": b"\xc9\xc3",
    "pop rdi; ret": b"\x5f\xc3",
    "pop rsi; pop r15; ret": b"\x5e\x41\x5f\xc3",
    "pop rdx; pop rXX": b"\x5a\x41",
    "xchg rsp": b"\x48\x87\xe4",
    "mov rsp, rbp": b"\x48\x89\xec",
}
for name, pat in pats.items():
    hits = []
    start = 0
    while True:
        i = d.find(pat, start)
        if i < 0:
            break
        a = to_addr(i)
        if a:
            hits.append(a)
        start = i + 1
        if len(hits) > 8:
            break
    print(f"{name:24} -> {[hex(x) for x in hits[:8]]}")
