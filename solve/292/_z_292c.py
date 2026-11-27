import sys, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
F = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\292_vuln"
d = open(F, "rb").read()
# segment executable : file off 0x1000, vaddr 0x08049000, size 0x663b0
OFF, VA, SZ = 0x1000, 0x08049000, 0x663b0
text = d[OFF:OFF + SZ]


def find(pattern, limit=3):
    out = []
    start = 0
    while len(out) < limit:
        i = text.find(pattern, start)
        if i < 0:
            break
        out.append(VA + i)
        start = i + 1
    return out


pats = {
    "pop eax; ret": b"\x58\xc3",
    "pop ebx; ret": b"\x5b\xc3",
    "pop ecx; ret": b"\x59\xc3",
    "pop edx; ret": b"\x5a\xc3",
    "int 0x80": b"\xcd\x80",
    "pop eax; pop ebx; ret": b"\x58\x5b\xc3",
    "xor eax,eax; ret": b"\x31\xc0\xc3",
}
for name, p in pats.items():
    addrs = find(p)
    print("%-24s %s" % (name, [hex(a) for a in addrs]))
