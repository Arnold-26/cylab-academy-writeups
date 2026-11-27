import struct, sys

path = sys.argv[1]
b = open(path, 'rb').read()
e = struct.unpack_from('<I', b, 0x3C)[0]
coff = e + 4
nsec = struct.unpack_from('<H', b, coff + 2)[0]
optsize = struct.unpack_from('<H', b, coff + 16)[0]
opt = coff + 20
ib = struct.unpack_from('<Q', b, opt + 24)[0]
secs = {}
sec = opt + optsize
for i in range(nsec):
    o = sec + i * 40
    name = b[o:o+8].rstrip(b'\0').decode('latin1')
    vsize, va, rawsize, rawptr = struct.unpack_from('<IIII', b, o + 8)
    secs[name] = (ib + va, vsize, rawptr, rawsize)

va, vsize, rawptr, rawsize = secs['.pdata']
pd = b[rawptr:rawptr+rawsize]
funcs = []
for i in range(0, len(pd) - 11, 12):
    beg, end, uw = struct.unpack_from('<III', pd, i)
    if beg == 0 and end == 0:
        continue
    funcs.append((ib + beg, ib + end, ib + uw))
funcs.sort(key=lambda t: t[1] - t[0], reverse=True)
print("nb fonctions:", len(funcs))
for s, en, uw in funcs[:12]:
    print("  %#x - %#x  taille=%d  unwind=%#x" % (s, en, en - s, uw))
print("...")
for s, en, uw in funcs[-5:]:
    print("  %#x - %#x  taille=%d" % (s, en, en - s))
