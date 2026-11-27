import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
F = r"/tmp/cylab_eps\292_vuln"
d = open(F, "rb").read()
OFF, VA, SZ = 0x1000, 0x08049000, 0x663b0
t = d[OFF:OFF + SZ]


def find(pattern, limit=4):
    out, start = [], 0
    while len(out) < limit:
        i = t.find(pattern, start)
        if i < 0:
            break
        out.append(VA + i)
        start = i + 1
    return out


pats = {
    "xor edx,edx; ret (31 d2 c3)": b"\x31\xd2\xc3",
    "xor edx,edx (31 d2)": b"\x31\xd2",
    "sub edx,edx; ret (29 d2 c3)": b"\x29\xd2\xc3",
    "cdq (99) + ret": b"\x99\xc3",
    "xor ecx,ecx; ret": b"\x31\xc9\xc3",
    "xor ebx,ebx; ret": b"\x31\xdb\xc3",
    "mov edx,0; ret (ba 00000000 c3)": b"\xba\x00\x00\x00\x00\xc3",
    "mov edx,ecx; ret (89 ca c3)": b"\x89\xca\xc3",
    "mov edx,ebx; ret (89 da c3)": b"\x89\xda\xc3",
}
for name, p in pats.items():
    print("%-34s %s" % (name, [hex(a) for a in find(p)]))
