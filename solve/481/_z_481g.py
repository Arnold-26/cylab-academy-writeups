import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{fl4g_h45_fl4ga947c25f}"
st, b = cy.req("GET", "/api/challenges/481/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 481, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"481 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(481, "flags are stepic", "Forensics", "", "steganographie avec l'outil stepic", f,
             "Le site liste 246 drapeaux de pays. L'un d'eux (`upz.png`) contient un message cache "
             "avec l'outil **stepic** (steganographie dans les pixels, pas de simple LSB). "
             "`stepic.decode()` revele le flag.")
