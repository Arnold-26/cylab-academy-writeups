import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
F = r"/tmp/cylab_eps\292_vuln"
d = open(F, "rb").read()
OFF, VA, SZ = 0x1000, 0x08049000, 0x663b0
t = d[OFF:OFF + SZ]


def safe(a):
    return b"\x0a" not in a.to_bytes(4, "little")


# mov eax, imm32 ; ret  ==  B8 xx xx xx xx C3
print("=== mov eax,imm32; ret ===")
res = []
for i in range(len(t) - 6):
    if t[i] == 0xB8 and t[i + 5] == 0xC3:
        val = int.from_bytes(t[i + 1:i + 5], "little")
        if val in (3, 11, 0, 59) and safe(VA + i):
            res.append((hex(VA + i), val))
print(res[:10])

print("=== gadgets 'pop eax ... ret' (max 10 octets) ===")
res2 = []
for i in range(len(t) - 2):
    if t[i] != 0x58:
        continue
    j = t.find(b"\xc3", i + 1, i + 11)
    if j < 0:
        continue
    if not safe(VA + i):
        continue
    res2.append((hex(VA + i), t[i:j + 1].hex()))
print(res2[:12])

print("=== 'xor eax,eax' suivi de ret proche ===")
res3 = []
for i in range(len(t) - 2):
    if t[i:i + 2] == b"\x31\xc0":
        j = t.find(b"\xc3", i + 2, i + 12)
        if j > 0 and safe(VA + i):
            res3.append((hex(VA + i), t[i:j + 1].hex()))
print(res3[:10])
