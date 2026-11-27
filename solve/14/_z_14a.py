import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{pining.for.the.fjords}"
st, b = cy.req("GET", "/api/challenges/14/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 14, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"14 droids1 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(14, "droids1", "Reverse Engineering", "", "XOR répétitif clé=mot de passe dans la lib native", f,
             "Le mot de passe est la ressource `password` = **`opossum`**. `fenugreek(input)` appelle "
             "`nutmeg(input)` (validation) puis `anise(input)`, qui fait "
             "`unscramble(data@0x1a3e, 0x1e, strdup(input), strlen(input))` : **la cle du XOR est "
             "l'input lui-meme**. Avec `opossum` on obtient `academy{pining.for.the.fjords}`.")
