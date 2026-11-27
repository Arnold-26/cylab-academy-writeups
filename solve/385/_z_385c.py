import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{g34r5_0f_m0r3_c95d6542}"
st, b = cy.req("GET", "/api/challenges/385/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 385, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"385 VM0 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(385, "Virtual Machine 0", "Reverse Engineering", "", "ratio d'engrenages LEGO -> hex -> ASCII", f,
             "Le zip contient `Virtual-Machine-0.dae`, un modele **COLLADA** d'un train d'engrenages LEGO. "
             "Les geometries portent les numeros de pieces (`3004`, `3700`, `18651`, `44237`, `3647`, "
             "`6098`, `99008`, `3649`) : les engrenages sont 40 dents (rouge, entree) et 8 dents (bleu, "
             "sortie), donc un **ratio 5:1**. `input.txt` donne un tres grand entier ; multiplier par 5, "
             "convertir en hexadecimale puis decoder en ASCII donne directement le flag. Les autres ratios "
             "(1, 8, 40, 3, 4) donnent du bruit binaire.")
