import sys, base64, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

enc = "NTczNDE3aDEzcl83aDRuXzdoM18xNDU3XzU4NTI3YmIyMjIK"
dec = base64.b64decode(enc).decode("utf-8", "replace").strip()
print("decode:", repr(dec))

cy = CyLab(delay=1.0)
cy.login()
cands = ["academy{%s}" % dec, dec, "academy{%s}" % dec.strip()]
ok = None
for c in cands:
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 721, "flag": c})
    try:
        o = json.loads(b).get("correct")
    except Exception:
        o = None
    print("%-50s -> %s" % (c, o))
    if o:
        ok = c
        break
print("FLAG:", ok)
