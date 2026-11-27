import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pefile
P = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\wine317\vuln.exe"
pe = pefile.PE(P)
d = open(P, "rb").read()
text = next(s for s in pe.sections if s.Name.startswith(b".text"))
tva, toff, tsize = text.VirtualAddress, text.PointerToRawData, text.Misc_VirtualSize
seg = d[toff:toff + tsize]
pat = b"\x46\x90\x40\x00"
i = 0
hits = []
while True:
    i = seg.find(pat, i)
    if i < 0:
        break
    hits.append(tva + i - 1)
    i += 1
print("occurrences de l'adresse 0x409046:", [hex(h) for h in hits])
for h in hits:
    o = h - tva
    print("\n--- contexte autour de 0x%x ---" % (0x400000 + h))
    print(seg[max(0, o - 24):o + 24].hex())
