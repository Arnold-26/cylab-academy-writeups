import sys, pathlib, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_z\415\challengefile")
d = p.read_bytes()
print("taille:", len(d))
print("debut:", d[:32].hex())
print("ascii:", "".join(chr(b) if 32 <= b < 127 else "." for b in d[:32]))
# essayer d'inverser par groupes de 4
for n in (4, 2, 8):
    out = bytearray()
    for i in range(0, len(d) - n + 1, n):
        out += d[i:i+n][::-1]
    out += d[len(out):]
    head = bytes(out[:8])
    print(f"swap {n}: {head.hex()} {head}")
    if head.startswith(b"\xff\xd8\xff") or head.startswith(b"\x89PNG"):
        out_path = p.with_suffix(f".swap{n}")
        out_path.write_bytes(bytes(out))
        print("  -> ecrit", out_path)
