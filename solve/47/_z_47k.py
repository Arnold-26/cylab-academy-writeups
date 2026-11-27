import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=1.0)
cy.login()
cands = ["encodedofvzaojsrs", "encodedofvzaojsrs{", "encodedofvzaojsrs ",
         "academy{encodedofvzaojsrs}", "cademy{encodedofvzaojsrs}"]
for f in cands:
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 47, "flag": f})
    try:
        ok = json.loads(b).get("correct")
    except Exception:
        ok = None
    print("%-32r -> %s" % (f, ok))
    if ok:
        print("FLAG:", f)
        break
