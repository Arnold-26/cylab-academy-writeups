import sys, struct, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = r"/tmp/cylab_eps\133_libc-2.27.so"
d = open(P, "rb").read()
# localiser la section .text (vaddr, offset, taille) via une lecture ELF simplifiee
import subprocess
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "readelf", "-SW",
                      "/tmp/cylab_eps/133_libc-2.27.so"],
                     capture_output=True, text=True).stdout
import re as _re
text = None
for line in out.splitlines():
    if "] .text" in line:
        parts = line.split()
        # [Nr] Name Type Address Off Size ...
        idx = parts.index(".text")
        addr = int(parts[idx + 2], 16)
        off = int(parts[idx + 3], 16)
        size = int(parts[idx + 4], 16)
        text = (addr, off, size)
        break
print("section .text:", text)
addr, off, size = text
seg = d[off:off + size]
gad = []
i = 0
while True:
    i = seg.find(b"\x5f\xc3", i)
    if i < 0:
        break
    gad.append(addr + i)
    i += 1
print("pop rdi; ret candidats:", [hex(g) for g in gad[:6]], "total", len(gad))
rets = []
i = 0
while len(rets) < 3:
    i = seg.find(b"\xc3", i)
    if i < 0:
        break
    rets.append(addr + i)
    i += 1
print("ret candidats:", [hex(r) for r in rets])
