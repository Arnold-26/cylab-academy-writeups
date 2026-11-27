import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
F = r"/tmp/cylab_eps\292_vuln"
d = open(F, "rb").read()
OFF, VA, SZ = 0x1000, 0x08049000, 0x663b0
t = d[OFF:OFF + SZ]


def addrs(pattern):
    out, i = [], 0
    while True:
        i = t.find(pattern, i)
        if i < 0:
            break
        out.append(VA + i)
        i += 1
    return out


def safe(a):
    return b"\x0a" not in a.to_bytes(4, "little") and b"\x00" not in a.to_bytes(4, "little")[:3]


for name, pat in (("pop eax; ret", b"\x58\xc3"), ("xor eax,eax; ret", b"\x31\xc0\xc3"),
                  ("pop ecx; ret", b"\x59\xc3"), ("pop ebx; ret", b"\x5b\xc3"),
                  ("int 0x80; ret", b"\xcd\x80\xc3"), ("inc eax; ret", b"\x40\xc3")):
    lst = addrs(pat)
    ok = [hex(a) for a in lst if safe(a)]
    print("%-20s total=%d  sans 0x0a: %s" % (name, len(lst), ok[:6]))
