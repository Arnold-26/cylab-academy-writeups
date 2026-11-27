import sys, json, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

enc = "+ikilmeqs:9?n8jijlim<=?98981jj:m>ik9j9;<iu"
dec = "".join(chr(ord(c) ^ 8) for c in enc)
print("decode:", dec)
f = dec.lstrip("#")
print("flag cand:", f)
cy = CyLab(delay=1.2)
cy.login()
for cand in (f, dec):
    st, b = cy.req("GET", "/api/challenges/131/")
    already = json.loads(b).get("solved_by_user")
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 131, "flag": cand})
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print(f"131 {cand} -> {ok}")
    if ok:
        if not already:
            wu.write(131, "Some Assembly Required 2", "Web Exploitation", "", "WASM + XOR 8", cand,
                     "Le JS obfusque charge un WASM (`aD8SvhyVkb`) dont `check_flag` compare l'entree a "
                     "une chaine encodee. Celle-ci est simplement **XOR 8** : "
                     "`+ikilmeqs:9?n8jijlim<=?98981jj:m>ik9j9;<iu` -> le flag.")
        break
