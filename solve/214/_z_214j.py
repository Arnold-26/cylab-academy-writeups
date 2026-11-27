import sys, struct, re, subprocess
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


def to_addr(fo):
    for v, o, s in segs:
        if o <= fo < o + s:
            return v + (fo - o)
    return None


pats = {
    "pop rdi; ret": b"\x5f\xc3",
    "pop rsi; ret": b"\x5e\xc3",
    "pop rdx; ret": b"\x5a\xc3",
    "pop rax; ret": b"\x58\xc3",
    "pop rdi; pop rbp; ret": b"\x5f\x5d\xc3",
    "pop rsi; pop r15; ret": b"\x5e\x41\x5f\xc3",
    "syscall": b"\x0f\x05",
    "leave; ret": b"\xc9\xc3",
    "pop rsp": b"\x5c",
    "mov rdi, rax": b"\x48\x89\xc7",
    "mov edi, eax": b"\x89\xc7",
    "mov rdi, rsp": b"\x48\x89\xe7",
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
        if len(hits) > 6:
            break
    print(f"{name:26} -> {[hex(x) for x in hits[:6]]}")
