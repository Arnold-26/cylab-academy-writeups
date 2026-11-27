import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=1.0)
cy.login()
body = "t1m3f1i3500000000000a8bbc8ed"
cands = [
    "academy{%s}" % body,
    "academy{t1m3f1l3500000000000a8bbc8ed}",
    "academy{%s}" % body.replace("i", "l"),
    "academy{%s}" % body.replace("f1i", "f1l"),
    body,
]
for f in cands:
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 36, "flag": f})
    try:
        ok = json.loads(b).get("correct")
    except Exception:
        ok = None
    print("%-52s -> %s" % (f[:52], ok))
    if ok:
        print("FLAG:", f)
        break
