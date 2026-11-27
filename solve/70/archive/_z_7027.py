import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=1.0)
cy.login()
tests = [
    (70, "f0und_1t_54c420aa"),
    (70, "academy{f0und_1t_54c420aa}"),
    (27, "An0tha_1_edc9a002"),
    (27, "academy{An0tha_1_edc9a002}"),
]
for cid, f in tests:
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": cid, "flag": f})
    try:
        ok = json.loads(b).get("correct")
    except Exception:
        ok = None
    print("%d %-34r -> %s" % (cid, f, ok))
