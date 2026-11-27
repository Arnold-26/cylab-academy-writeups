import sys, re, json, time, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
urllib3.disable_warnings()
cy = CyLab(delay=0.4)
cy.login()
for cid in (494, 478):
    cy.req("PUT", f"/api/challenges/{cid}/instance/?source=library")
    base = None
    desc = ""
    for _ in range(10):
        time.sleep(0.8)
        st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
        d = json.loads(b) if b.startswith("{") else {}
        desc = d.get("description") or ""
        m = re.search(r"(https?://[A-Za-z0-9.\-]+:\d+)", desc)
        if m:
            base = m.group(1).rstrip("/") + "/"
            break
    print("=== %d === base=%s" % (cid, base))
    print("desc:", desc[:250].replace("\n", " "))
    if not base:
        continue
    for k in range(4):
        try:
            r = requests.get(base, timeout=15)
            print("status:", r.status_code, "| len:", len(r.text))
            m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
            print("flag dans le HTML:", m.group(0) if m else None)
            for mm in re.finditer(r"<!--.*?-->", r.text, re.S):
                print("   commentaire:", mm.group(0)[:200])
            break
        except Exception:
            time.sleep(1.5)
