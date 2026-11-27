# 300 - Sleuthkit Apprentice  (Forensics, picoCTF 2022)
# Flag: academy{by73_5urf3r_6395be48}
# Write-up: ../../../writeups/forensics/300-sleuthkit-apprentice.md
# Script exact utilise pour produire le flag.
#
import struct, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
path = r"./_z_wad300u\WinAntiDbg0x300.exe"
d = open(path, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
imagebase = struct.unpack_from("<I", d, pe + 24 + 28)[0]
o = pe + 24 + optsz
secs = []
for i in range(nsec):
    name = d[o:o + 8].rstrip(b"\0").decode(errors="replace")
    vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", d, o + 8)
    secs.append((name, vaddr, vsize, rawptr, rawsize))
    o += 40


def va_of(off):
    for (name, vaddr, vsize, rawptr, rawsize) in secs:
        if rawptr <= off < rawptr + rawsize:
            return imagebase + vaddr + (off - rawptr)
    return None


needles = [b"Welcome to the 0x300", b"OutputDebugStringW", b"DebugActiveProcess", b"pdb"]
for nd in needles:
    for m in re.finditer(re.escape(nd), d):
        va = va_of(m.start())
        print("%-24r file=0x%x va=%s" % (nd, m.start(), ("0x%08x" % va) if va else None))
