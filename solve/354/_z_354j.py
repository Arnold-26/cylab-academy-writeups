import sys, zipfile, io, re, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
src = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_iw\output.bmp")
data = src.read_bytes()
out = bytearray()
i = 0x8C
while i + 1 < len(data):
    chunk = data[i:i + 2]
    if chunk == b"\xff\x00":
        break
    out += chunk
    i += 4
print("zip taille:", len(out), "debut:", bytes(out[:8]))
zpath = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_iw\extracted.zip")
zpath.write_bytes(bytes(out))
try:
    z = zipfile.ZipFile(io.BytesIO(bytes(out)))
    print("noms:", z.namelist())
    for n in z.namelist():
        content = z.read(n)
        txt = content.decode("utf-8", "replace")
        print(f"\n=== {n} ({len(content)} o) ===")
        print(txt[:300])
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        if m:
            print("\nFLAG:", m.group(0))
except Exception as e:
    print("err zip:", type(e).__name__, e)
