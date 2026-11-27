import sys, requests, urllib3, pathlib, tarfile
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
u = "https://challenge-files.cylabacademy.net/library/dba3b2b6509571cde1943da76de60faa81bdef15008096d1e80a733ef898bfc9/distribution.tgz"
dest = B / "190_dist.tgz"
if not dest.exists() or dest.stat().st_size < 1000:
    r = requests.get(u, timeout=120, verify=False)
    dest.write_bytes(r.content)
print("taille:", dest.stat().st_size)
out = B / "bithug"
out.mkdir(exist_ok=True)
try:
    with tarfile.open(dest) as t:
        t.extractall(out)
    for p in sorted(out.rglob("*")):
        if p.is_file():
            print("%-55s %d" % (str(p.relative_to(out))[:55], p.stat().st_size))
except Exception as e:
    print("err", type(e).__name__, str(e)[:120])
