import sys, subprocess, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BIN = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\36_no_auth_mistery"
OUT = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\36_investigation-encoded-2-output"
d = open(BIN, "rb").read()
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "readelf", "-SW",
                      "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/36_no_auth_mistery"],
                     capture_output=True, text=True).stdout
ro = None
for line in out.splitlines():
    if "] .rodata" in line:
        p = line.split()
        i = p.index(".rodata")
        ro = (int(p[i + 2], 16), int(p[i + 3], 16))
        break
print("rodata (vaddr, off):", [hex(x) for x in ro])
va, off = ro


def get(addr, n):
    o = off + (addr - va)
    return d[o:o + n]


secret = get(0x1300, 71)
idx_tab = list(struct.unpack("<38i", get(0x1360, 152)))
print("secret:", secret.hex())
print("indexTable[0:10]:", idx_tab[:10], "... max:", max(idx_tab))


def bit(i):
    return (secret[i // 8] >> (7 - i % 8)) & 1


codes = {}
for ns in range(37):
    a, b = idx_tab[ns], idx_tab[ns + 1]
    if not (0 <= a <= b <= len(secret) * 8):
        continue
    codes["".join(str(bit(i)) for i in range(a, b))] = ns
print("codes:", len(codes))

enc = open(OUT, "rb").read()
print("output:", len(enc), "octets")
bitstr = "".join(format(x, "08b") for x in enc)
res = []
i = 0
while i < len(bitstr):
    hit = None
    for L in range(1, 40):
        if i + L > len(bitstr):
            break
        seg = bitstr[i:i + L]
        if seg in codes:
            hit = (L, codes[seg])
            break
    if hit is None:
        break
    L, ns = hit
    if ns < 26:
        ch = chr(ord("a") + ns)
    elif ns < 36:
        ch = chr(ord("0") + (ns - 26))
    else:
        ch = " "
    res.append(ch)
    i += L
txt = "".join(res)
print("decode:", repr(txt))
import re
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", m.group(0) if m else None)
