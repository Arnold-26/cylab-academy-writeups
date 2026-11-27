import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{v4lua4bl3_1npu7_6fd920cb}"
st, b = cy.req("GET", "/api/challenges/138/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 138, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"138 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(138, "What's your input?", "Binary Exploitation", "", "injection Python 2 input()", f,
             "Le service tourne en **Python 2.7** et utilise `input()`, qui **evalue** la saisie comme "
             "du code Python. Il suffit d'envoyer `__import__('os').system('cat flag')` a l'invite "
             "`City?` pour afficher le flag (le resultat de `system` est 0, donc la comparaison with "
             "`city` echoue, mais le flag est deja imprime).")
