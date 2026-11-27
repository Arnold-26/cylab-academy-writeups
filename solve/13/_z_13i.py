import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.9)
cy.login()
inner = "n3xt_0n30000000000000000000000000cc361e70"
cands = ["academy{%s}" % inner, inner, "academy{n3xt_0n3_cc361e70}",
         "academy{n3xt_0n300cc361e70}"]
for f in cands:
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 13, "flag": f})
    try:
        ok = json.loads(b).get("correct")
    except Exception:
        ok = None
    print("%-56r -> %s" % (f[:56], ok))
    if ok:
        break
