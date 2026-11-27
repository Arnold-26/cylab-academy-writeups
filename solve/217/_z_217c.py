import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
data = open("/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/217_homework", "rb").read()
# le fichier est un ELF : vaddr 0x5260 -> offset fichier
import struct
phoff = struct.unpack_from("<Q", data, 0x20)[0]
phentsize = struct.unpack_from("<H", data, 0x36)[0]
phnum = struct.unpack_from("<H", data, 0x38)[0]
segs = []
for i in range(phnum):
    off = phoff + i * phentsize
    p_type = struct.unpack_from("<I", data, off)[0]
    p_offset = struct.unpack_from("<Q", data, off + 8)[0]
    p_vaddr = struct.unpack_from("<Q", data, off + 16)[0]
    p_filesz = struct.unpack_from("<Q", data, off + 32)[0]
    if p_type == 1:
        segs.append((p_vaddr, p_offset, p_filesz))


def to_off(va):
    for v, o, s in segs:
        if v <= va < v + s:
            return o + (va - v)
    return None


off = to_off(0x5260)
print("board offset:", hex(off) if off else None)
if off:
    board = data[off:off + 50 * 22]
    for r in range(50):
        row = board[r * 22:(r + 1) * 22]
        txt = "".join(chr(c) if 32 <= c < 127 else "." for c in row)
        print(f"{r:2d} |{txt}|")
    print("\n=== rows/cols globals ===")
    print("rows:", struct.unpack_from("<I", data, to_off(0x56ac))[0])
    print("cols:", struct.unpack_from("<I", data, to_off(0x56b0))[0])
