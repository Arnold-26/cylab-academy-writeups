import sys, json, hashlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=1.2)
cy.login()
cands = []
for k in ("9d74d90d", "9d74d90d", "00000000"):
    cands.append(f"academy{{br1ng_y0ur_0wn_k3y_{k}}}")
# essais classiques de cles
for key in ("academy", "picoCTF", "key", "license", "academy{", "br1ng_y0ur_0wn_k3y"):
    cands.append("academy{br1ng_y0ur_0wn_k3y_" + hashlib.md5(key.encode()).hexdigest() + "}")
seen = set()
for f in cands:
    if f in seen:
        continue
    seen.add(f)
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 276, "flag": f})
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print(f"276 {f} -> {ok}")
    if ok:
        break
