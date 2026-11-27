import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

inner = "1_533_3_n4m35_a1eed517"
cy = CyLab(delay=1.0)
cy.login()
cands = ["academy{%s}" % inner, "picoCTF{%s}" % inner, inner]
ok = None
for c in cands:
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 413, "flag": c})
    try:
        o = json.loads(b).get("correct")
    except Exception:
        o = None
    print("%-40s -> %s" % (c, o))
    if o:
        ok = c
        break
print("FLAG:", ok)
