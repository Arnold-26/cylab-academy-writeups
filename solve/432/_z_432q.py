import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
src = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\432_original.jpg"
dst = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\432_patched.jpg"
d = bytearray(open(src, "rb").read())
print("taille:", len(d))
# 1) les 3 dates principales
old = b"2023:11:20 15:46:23"
new = b"1970:01:01 00:00:00"
n1 = d.count(old)
d = bytearray(bytes(d).replace(old, new))
print("dates remplacees:", n1)
# 2) les 3 sous-secondes '703' aux offsets connus
for off in (688, 700, 712):
    print("  subsec @%d: %r -> '001'" % (off, bytes(d[off:off + 3])))
    d[off:off + 3] = b"001"
# 3) Samsung TimeStamp (epoch ms) a 0x2b83e0 : '1700513181420' -> '1' + NUL
off3 = 0x2b83e0
print("  samsung @0x%x: %r" % (off3, bytes(d[off3:off3 + 13])))
assert bytes(d[off3:off3 + 13]) == b"1700513181420", "valeur inattendue"
d[off3:off3 + 13] = b"1" + b"\x00" * 12
open(dst, "wb").write(bytes(d))
print("ecrit:", dst, len(d))
