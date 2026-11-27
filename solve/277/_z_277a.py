import sys, re, requests, urllib3, pathlib, tarfile, io
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
u = "https://challenge-files.cylabacademy.net/library/3c9da3abf15f369ce7add72b013b737dd8dcd20d0839d3e87901cb6319ffd70c/bundle.tar.gz"
dest = B / "277_bundle.tar.gz"
if not dest.exists() or dest.stat().st_size < 100:
    r = requests.get(u, timeout=90, verify=False)
    dest.write_bytes(r.content)
print("taille:", dest.stat().st_size)
out = B / "liveart"
out.mkdir(exist_ok=True)
with tarfile.open(dest, "r:gz") as t:
    t.extractall(out)
for p in out.rglob("*"):
    if p.is_file():
        print("%-50s %d" % (str(p.relative_to(out)), p.stat().st_size))
