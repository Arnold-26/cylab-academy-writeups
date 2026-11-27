import sys, json, re, time, pathlib, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=1.2)
cy.login()
BASE = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_bin")
st, b = cy.req("GET", "/api/challenges/441/instance/")
d = json.loads(b) if b.startswith("{") else {}
desc = d.get("description") or ""
urls = [u for u in re.findall(r"https?://[^\s'\"<>]+", desc) if "challenge-files" in u]
print("urls:", urls)
for u in urls:
    name = u.rsplit("/", 1)[-1]
    dest = BASE / f"441_{name}"
    if dest.exists() and dest.stat().st_size > 0:
        print("deja:", name, dest.stat().st_size)
        continue
    for attempt in range(3):
        try:
            r = requests.get(u, timeout=180, verify=False)
            dest.write_bytes(r.content)
            print("ok:", name, len(r.content))
            break
        except Exception as e:
            print("err", name, type(e).__name__)
            time.sleep(2)
