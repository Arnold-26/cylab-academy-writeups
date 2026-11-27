import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
F = r"/tmp/cylab_eps\292_vuln"
d = open(F, "rb").read()
OFF, VA, SZ = 0x1000, 0x08049000, 0x663b0
t = d[OFF:OFF + SZ]


def safe(a):
    return b"\x0a" not in a.to_bytes(4, "little")


print("=== add eax, imm32; ret (05 xx.. c3) ===")
r = []
for i in range(len(t) - 6):
    if t[i] == 0x05 and t[i + 5] == 0xC3:
        v = int.from_bytes(t[i + 1:i + 5], "little")
        if safe(VA + i):
            r.append((hex(VA + i), v))
print(r[:12])

print("=== add eax, imm8; ret (83 c0 XX c3) ===")
r2 = []
for i in range(len(t) - 4):
    if t[i:i + 2] == b"\x83\xc0" and t[i + 3] == 0xC3:
        if safe(VA + i):
            r2.append((hex(VA + i), t[i + 2]))
print(r2[:12])

print("=== inc eax (40) suivi de ret ===")
r3 = []
for i in range(len(t) - 1):
    if t[i] == 0x40 and t[i + 1] == 0xC3 and safe(VA + i):
        r3.append(hex(VA + i))
print(r3[:10])
