import struct, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"D:\ctf-index\_z_wad300u\WinAntiDbg0x300.exe"
d = open(p, "rb").read()
asm = open(r"D:\ctf-index\_z_wad300u\_300.asm", encoding="utf-8", errors="replace").read()

for va in (0x408d94, 0x408e50, 0x408dc0):
    pat = struct.pack("<I", va)
    idx = [m.start() for m in re.finditer(re.escape(pat), d)]
    print("ptr to %#x at file offsets" % va, [hex(i) for i in idx[:5]])
    print("  asm hits for %x:" % va, asm.count("%x" % va))
