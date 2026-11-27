import sys, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p1 = "/tmp/cylab_eps/220_breadth.v1"
p2 = "/tmp/cylab_eps/220_breadth.v2"


def read_cstr(path, fo, n=200):
    d = open(path, "rb").read()
    s = d[fo:fo + n].split(b"\x00")[0]
    return s


for fo in (0x155ec8, 0x155ef8, 0x155ea0, 0x155f10):
    print(f"0x{fo:x} v1: {read_cstr(p1, fo)[:120]}")
    print(f"0x{fo:x} v2: {read_cstr(p2, fo)[:120]}")
# chercher un flag dans les deux binaires
import re
for name, path in (("v1", p1), ("v2", p2)):
    d = open(path, "rb").read()
    for m in re.finditer(rb"(?:academy|picoCTF)\{[^}]{4,120}\}", d):
        print(name, "FLAG:", m.group(0))
