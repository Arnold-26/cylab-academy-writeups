import sys, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
dest = B / "529_pico-bank.apk"
if not (dest.exists() and dest.stat().st_size > 100000):
    r = requests.get("http://chatelaine.cylabacademy.net:48796/download/pico-bank.apk",
                     timeout=180, verify=False)
    dest.write_bytes(r.content)
print("taille:", dest.stat().st_size)
