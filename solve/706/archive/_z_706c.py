import sys, zlib, pathlib, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = pathlib.Path("/tmp/repo706")
objdir = base / "objects"
files = [p for p in objdir.rglob("*") if p.is_file()]
print("objets:", len(files))
FLAG = re.compile(rb"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
for f in files:
    data = f.read_bytes()
    try:
        dec = zlib.decompress(data)
    except Exception:
        continue
    kind = dec.split(b" ", 1)[0]
    m = FLAG.search(dec)
    if m:
        print(f"\n=== {f.name} ({kind}) ===")
        print("FLAG:", m.group(0).decode())
    if kind in (b"commit", b"tag"):
        print(f"\n=== {f.name} ({kind}) ===")
        print(dec[:400])
    elif kind == b"blob" and b"flag" in dec.lower():
        print(f"\n=== blob {f.name} ===")
        print(dec[:300])
