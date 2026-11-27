import sys, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = "/tmp/cylab_eps/220_breadth.v1"
d = open(p, "rb").read()
# contexte autour de 0x253753 (probable chaine de version)
s = d[0x253740:0x253780]
print("contexte 0x253753:", s)
# contexte autour de 0x9504b : convertir en vaddr via les phdr
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


def to_va(fo):
    for v, o, sz in segs:
        if o <= fo < o + sz:
            return v + (fo - o)
    return None


for fo in (0x9504b, 0x9504e, 0x253753):
    print(f"fichier 0x{fo:x} -> vaddr {hex(to_va(fo)) if to_va(fo) else None}")
# desassembler autour
import subprocess
va = to_va(0x95040)
if va:
    r = subprocess.run(["objdump", "-d", "-Mintel", f"--start-address={va-0x20}", f"--stop-address={va+0x40}", p],
                       capture_output=True, text=True)
    print(r.stdout[-2500:])
