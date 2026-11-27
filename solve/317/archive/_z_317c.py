import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pefile, struct
P = r"/tmp/cylab_eps\wine317\vuln.exe"
pe = pefile.PE(P)
d = open(P, "rb").read()
# .text
text = next(s for s in pe.sections if s.Name.startswith(b".text"))
tva, toff, tsize = text.VirtualAddress, text.PointerToRawData, text.Misc_VirtualSize
seg = d[toff:toff + tsize]
pat = b"\x68\x46\x90\x40\x00"  # push 0x409046
i = 0
hits = []
while True:
    i = seg.find(pat, i)
    if i < 0:
        break
    hits.append(tva + i)
    i += 1
print("references a flag.txt:", [hex(h) for h in hits])
# afficher le debut de la fonction contenant la reference (prologue le plus proche)
for h in hits[:3]:
    start = h
    # remonter jusqu'a un prologue push ebp; mov ebp,esp
    for j in range(h, max(tva, h - 0x400), -1):
        o = j - tva
        if seg[o:o + 3] == b"\x55\x89\xe5":
            start = j
            break
    print("fonction autour de %s : debut probable 0x%x (RVA 0x%x)" % (hex(h), 0x400000 + start, start))
