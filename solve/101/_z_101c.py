import sys, base64, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

b = "YWNhZGVteXttNGNyMHNfcl9kNG5nM3IwdXN9"
dec = base64.b64decode(b + "=" * (-len(b) % 4)).decode()
print("decode:", dec)
cy = CyLab(delay=1.2)
cy.login()
st, b2 = cy.req("GET", "/api/challenges/101/")
already = json.loads(b2).get("solved_by_user")
st, b2 = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 101, "flag": dec})
ok = json.loads(b2).get("correct") if b2.startswith("{") else None
print(f"101 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(101, "Weird File", "Forensics", "", "macro VBA en base64", dec,
             "Le `.docm` contient un `vbaProject.bin` dont la macro appelle "
             "`Shell(\"python -c 'print(...)'\")` avec une chaine **base64** : "
             "`YWNhZGVteXttNGNyMHNfcl9kNG5nM3IwdXN9` se decode en flag.")
