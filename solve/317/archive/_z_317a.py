import sys, zipfile, pathlib, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"/tmp/cylab_eps")
z = B / "317_vuln.zip"
out = B / "wine317"
out.mkdir(exist_ok=True)
try:
    with zipfile.ZipFile(z) as f:
        for n in f.namelist():
            f.extract(n, out, pwd=b"academy")
        print("fichiers:", f.namelist())
except Exception as e:
    print("err", type(e).__name__, str(e)[:100])
for p in out.rglob("*"):
    if p.is_file():
        print("%-40s %d" % (p.name, p.stat().st_size))
print("\n=== infos PE ===")
import pefile
for p in out.rglob("*.exe"):
    pe = pefile.PE(str(p))
    print(p.name, "| machine:", hex(pe.FILE_HEADER.Machine),
          "| imagebase:", hex(pe.OPTIONAL_HEADER.ImageBase),
          "| DllCharacteristics:", hex(pe.OPTIONAL_HEADER.DllCharacteristics))
    for s in pe.sections:
        print("   section", s.Name.decode(errors="replace").strip("\x00"),
              hex(s.VirtualAddress), hex(s.Misc_VirtualSize), hex(s.Characteristics))
