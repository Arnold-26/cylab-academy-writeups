import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
body = "468293b06253c715005873e333d98dbc"
for f in (f"academy{{{body}}}", body):
    st, b = cy.req("GET", "/api/challenges/148/")
    already = json.loads(b).get("solved_by_user")
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 148, "flag": f})
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print(f"148 {f} -> {ok}")
    if ok:
        if not already:
            wu.write(148, "New Vignere", "Cryptography", "", "cryptanalyse par contraintes de format", f,
                     "Chiffrement = **b16** (chaque octet encode en deux caracteres parmi 16) puis "
                     "**Vigenere** sur un alphabet de 16 lettres. Le flag ne contient que "
                     "`abcdef0123456789`, donc chaque position paire du clair b16 vaut `d` ou `g` et "
                     "chaque position impaire `a`-`j`. Ces contraintes determinant la cle "
                     "(`bickhknij`, longueur 9) sans brute force exhaustif.")
        break
