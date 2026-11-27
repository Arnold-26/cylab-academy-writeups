import sys, re, json, time, requests, urllib3, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
cy = CyLab(delay=0.4)
cy.login()
for cid in (153,):
    cy.req("PUT", f"/api/challenges/{cid}/instance/?source=library")
    base = None
    for _ in range(12):
        time.sleep(0.8)
        st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
        d = json.loads(b) if b.startswith("{") else {}
        m = re.search(r"(http://[A-Za-z0-9.\-]+:\d+/)", d.get("description") or "")
        if m:
            base = m.group(1)
            break
    print("base:", base)
    if not base:
        continue
    # retry agressif
    html = None
    for k in range(10):
        try:
            r = requests.get(base + "index.html", timeout=15)
            html = r.text
            print("index:", r.status_code, len(html))
            break
        except Exception as e:
            time.sleep(1.5)
    if not html:
        print("impossible de joindre")
        continue
    print(html[:400])
    for u in set(re.findall(r"[\w./-]+\.(?:wasm|js)", html)):
        for k in range(3):
            try:
                rr = requests.get(base + u.lstrip("/"), timeout=30)
                dest = B / f"{cid}_{u.rsplit('/',1)[-1]}"
                dest.write_bytes(rr.content)
                print("ok", dest.name, len(rr.content))
                break
            except Exception as e:
                time.sleep(1)
