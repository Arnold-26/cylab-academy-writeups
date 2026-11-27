import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
F = r"/tmp/cylab_eps\292_vuln"
d = open(F, "rb").read()
OFF, VA, SZ = 0x1000, 0x08049000, 0x663b0
t = d[OFF:OFF + SZ]
# gadgets commencant par 0x5A (pop edx) et se terminant par un ret dans les 12 octets
res = []
for i in range(len(t) - 2):
    if t[i] != 0x5A:
        continue
    j = t.find(b"\xc3", i + 1, i + 12)
    if j < 0:
        continue
    if b"\xe8" in t[i:j] or b"\xc2" in t[i:j]:
        continue
    res.append((VA + i, t[i:j + 1].hex()))
print("gadgets 'pop edx ... ret':", len(res))
for a, h in res[:15]:
    print("  %s : %s" % (hex(a), h))
# aussi les sequences 'xor edx,edx' suivies d'un ret proche
res2 = []
for i in range(len(t) - 3):
    if t[i:i + 2] == b"\x31\xd2":
        j = t.find(b"\xc3", i + 2, i + 14)
        if j > 0:
            res2.append((VA + i, t[i:j + 1].hex()))
print("gadgets 'xor edx,edx ... ret':", len(res2))
for a, h in res2[:10]:
    print("  %s : %s" % (hex(a), h))
