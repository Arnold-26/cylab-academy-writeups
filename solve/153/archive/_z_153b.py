import sys, re, requests, urllib3, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
BASE = "http://chatelaine.cylabacademy.net:25859/"
r = requests.get(BASE + "index.html", timeout=20)
print("index:", r.status_code, len(r.text))
print(r.text[:600])
for u in re.findall(r"[\w./-]+\.(?:wasm|js)", r.text):
    url = BASE + u.lstrip("/")
    try:
        rr = requests.get(url, timeout=30)
        dest = B / f"153_{u.rsplit('/',1)[-1]}"
        dest.write_bytes(rr.content)
        print("ok", dest.name, len(rr.content))
    except Exception as e:
        print("err", u, type(e).__name__)
