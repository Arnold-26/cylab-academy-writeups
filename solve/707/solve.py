# 707 - Forensics Git 2  (Forensics, picoCTF 2026)
# Flag: academy{g17_r35cu3_16ac6bf3}
# Write-up: ../../../writeups/forensics/707-forensics-git-2.md
# Script exact utilise pour produire le flag.
#
import sys, zlib, pathlib, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = pathlib.Path("/tmp/repo707/.git/objects")
if not base.exists():
    base = pathlib.Path("/tmp/repo707")
print("base:", base, base.exists())
FLAG = re.compile(rb"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
files = [p for p in base.rglob("*") if p.is_file()]
print("fichiers:", len(files))
found = []
for f in files:
    data = f.read_bytes()
    # objet git : zlib
    try:
        dec = zlib.decompress(data)
    except Exception:
        dec = data
    m = FLAG.search(dec)
    if m:
        print(f"FLAG dans {f}: {m.group(0).decode()}")
        found.append(m.group(0).decode())
        continue
    # chercher du texte lisible contenant 'flag'
    if b"flag" in dec.lower():
        i = dec.lower().find(b"flag")
        print(f"{f.name}: ...{dec[max(0,i-80):i+120]!r}")
if found:
    print("TOTAL flags:", found)
else:
    print("aucun flag direct")
