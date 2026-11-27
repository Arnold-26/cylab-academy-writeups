import sys, re, json, time, requests, urllib3, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
urllib3.disable_warnings()
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/413/instance/?source=library")
desc = ""
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/413/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    if "challenge-files" in desc:
        break
print(desc[:400].replace("\n", " "))
for u in re.findall(r"https?://[^\s'\"<>]+", desc):
    if "challenge-files" not in u:
        continue
    name = u.rsplit("/", 1)[-1]
    dest = B / f"413_{name}"
    for attempt in range(3):
        try:
            r = requests.get(u, timeout=180, verify=False, stream=True)
            total = 0
            with open(dest, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
                    total += len(chunk)
                    if total > 80 * (1 << 20):
                        break
            print("ok", dest.name, total)
            break
        except Exception as e:
            print("essai", attempt + 1, type(e).__name__)
            time.sleep(3)
