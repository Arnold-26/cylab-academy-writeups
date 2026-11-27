import sys, zlib, pathlib, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = pathlib.Path("/tmp/repo705")
files = [p for p in base.rglob("*") if p.is_file()]
print("fichiers:", len(files), [str(p.relative_to(base)) for p in files])
FLAG = re.compile(rb"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
for f in files:
    data = f.read_bytes()
    try:
        dec = zlib.decompress(data)
    except Exception:
        dec = data
    print(f"\n=== {f.name} ({len(data)} o -> {len(dec)}) ===")
    print(dec[:400])
    m = FLAG.search(dec)
    if m:
        print("FLAG:", m.group(0).decode())
