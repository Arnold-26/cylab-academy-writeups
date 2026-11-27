import sys, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = "/tmp/cylab_eps/217_homework"
d = open(p, "rb").read()
phoff = struct.unpack_from("<Q", d, 0x20)[0]
phentsize = struct.unpack_from("<H", d, 0x36)[0]
phnum = struct.unpack_from("<H", d, 0x38)[0]
segs = []
for i in range(phnum):
    off = phoff + i * phentsize
    if struct.unpack_from("<I", d, off)[0] == 1:
        segs.append((struct.unpack_from("<Q", d, off + 16)[0],
                     struct.unpack_from("<Q", d, off + 8)[0],
                     struct.unpack_from("<Q", d, off + 32)[0]))


def off_of(va):
    for v, o, s in segs:
        if v <= va < v + s:
            return o + (va - v)
    return None


TABLE = 0x309C
base_off = off_of(TABLE)
print("table offset:", hex(base_off))
raw = d[base_off:base_off + 0x5C * 4]
for ch in "0123456789+-*/%!`><^v_|\\$.,#gp&~\"@: ":
    idx = ord(ch) - 0x21
    if 0 <= idx < 0x5C:
        val = struct.unpack_from("<i", raw, idx * 4)[0]
        target = (TABLE + val) & 0xFFFFFFFFFFFFFFFF
        print(f"  {ch!r} (0x{ord(ch):02x}) idx {idx:2d} -> 0x{target:x}")
