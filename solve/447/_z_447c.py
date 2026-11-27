import sys, requests, urllib3, pathlib, tarfile, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
u = "https://challenge-files.cylabacademy.net/library/cba800142097728c5bade965cb5528499ac15c6c2513002dba378ea714c757c3/elements.tar.gz"
dest = B / "447_elements.tgz"
r = requests.get(u, timeout=90, verify=False)
dest.write_bytes(r.content)
print("taille:", dest.stat().st_size)
out = B / "elements"
out.mkdir(exist_ok=True)
with tarfile.open(dest) as t:
    t.extractall(out)
for p in sorted(out.rglob("*")):
    if p.is_file():
        print("  ", str(p.relative_to(out))[:60], p.stat().st_size)
# chercher le flag / la logique
pat = re.compile(rb"(?:academy|picoCTF)\{[^}]{2,120}\}")
for p in out.rglob("*"):
    if p.is_file() and p.stat().st_size < 300000:
        d = p.read_bytes()
        for m in pat.finditer(d):
            print("FLAG dans", p.name, ":", m.group(0).decode("latin-1"))
