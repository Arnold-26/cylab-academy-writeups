import sys, re, requests, urllib3, pathlib, tarfile
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
u = "https://challenge-files.cylabacademy.net/library/05811f9f3ba7253920faabd5a8b2308ee44ade0e89a016380957f654cb168262/server.tar.gz"
dest = B / "494_server.tar.gz"
r = requests.get(u, timeout=90, verify=False)
dest.write_bytes(r.content)
print("taille:", dest.stat().st_size)
out = B / "pachinko"
out.mkdir(exist_ok=True)
try:
    with tarfile.open(dest) as t:
        t.extractall(out)
    for p in sorted(out.rglob("*")):
        if p.is_file():
            print("  ", str(p.relative_to(out))[:60], p.stat().st_size)
except Exception as e:
    print("err", type(e).__name__, str(e)[:100])
