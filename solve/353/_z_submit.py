import sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

pairs = []
for a in sys.argv[1:]:
    cid, flag = a.split("=", 1)
    pairs.append((int(cid), flag))
cy = CyLab(delay=1.5)
cy.login()
for cid, flag in pairs:
    for attempt in range(3):
        st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": cid, "flag": flag})
        try:
            d = json.loads(b)
        except Exception:
            print(cid, "non-JSON", st, b[:200])
            time.sleep(2)
            continue
        print("%d -> correct=%s %s" % (cid, d.get("correct"), json.dumps(d)[:300]))
        if d.get("correct"):
            break
        time.sleep(1)
