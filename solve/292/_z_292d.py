import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
F = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\292_vuln"
d = open(F, "rb").read()
OFF, VA, SZ = 0x1000, 0x08049000, 0x663b0
text = d[OFF:OFF + SZ]


def find(pattern, limit=4):
    out, start = [], 0
    while len(out) < limit:
        i = text.find(pattern, start)
        if i < 0:
            break
        out.append(VA + i)
        start = i + 1
    return out


pats = {
    "pop edx; pop ebx; ret": b"\x5a\x5b\xc3",
    "pop edx; pop ecx; ret": b"\x5a\x59\xc3",
    "pop edx; pop esi; ret": b"\x5a\x5e\xc3",
    "pop edx; pop edi; ret": b"\x5a\x5f\xc3",
    "pop edx; pop ebp; ret": b"\x5a\x5d\xc3",
    "pop edx; pop edx; ret": b"\x5a\x5a\xc3",
    "pop edx; ret32": b"\x5a\xc3",
    "mov edx, eax; ...": b"\x89\xc2",
    "pop esi; ret": b"\x5e\xc3",
    "pop edi; ret": b"\x5f\xc3",
}
for name, p in pats.items():
    print("%-26s %s" % (name, [hex(a) for a in find(p)]))
