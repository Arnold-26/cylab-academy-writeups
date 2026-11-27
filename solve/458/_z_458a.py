import sys, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
u = "https://challenge-files.cylabacademy.net/library/4c086b6045c5f2b5200e1ef7ff1daace7008f76e3614bc1d98e6fda8863c43c2/perplexed"
dest = B / "458_perplexed"
if not (dest.exists() and dest.stat().st_size > 1000):
    r = requests.get(u, timeout=60, verify=False)
    dest.write_bytes(r.content)
print("taille:", dest.stat().st_size)
