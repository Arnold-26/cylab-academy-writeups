import sys, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
u = "https://challenge-files.cylabacademy.net/library/3e5f432811e9761c626e2a6ea7b82e48b8db94a330816a2962c7fe4371532376/cheese_list.txt"
dest = B / "474_cheese_list.txt"
if not (dest.exists() and dest.stat().st_size > 50):
    r = requests.get(u, timeout=60, verify=False)
    dest.write_bytes(r.content)
txt = dest.read_text(errors="replace")
lines = [l.strip() for l in txt.splitlines() if l.strip()]
print("taille:", dest.stat().st_size, "| lignes:", len(lines))
print("exemples:", lines[:15])
