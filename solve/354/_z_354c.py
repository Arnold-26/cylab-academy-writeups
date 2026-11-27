import sys, struct, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_iw\output.bmp")
d = p.read_bytes()
print("taille:", len(d))
print("signature:", d[:2])
size = struct.unpack_from("<I", d, 2)[0]
offset = struct.unpack_from("<I", d, 10)[0]
hdr_size = struct.unpack_from("<I", d, 14)[0]
w = struct.unpack_from("<i", d, 18)[0]
h = struct.unpack_from("<i", d, 22)[0]
planes = struct.unpack_from("<H", d, 26)[0]
bpp = struct.unpack_from("<H", d, 28)[0]
comp = struct.unpack_from("<I", d, 30)[0]
imgsize = struct.unpack_from("<I", d, 34)[0]
print(f"size={size} offset={offset} hdr={hdr_size} w={w} h={h} planes={planes} bpp={bpp} comp={comp} imgsize={imgsize}")
print("octets 34-60:", d[34:60].hex())
