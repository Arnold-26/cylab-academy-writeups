import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{899f655514ccb5662bac39d1f53ec6bd}"
st, b = cy.req("GET", "/api/challenges/29/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 29, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"29 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(29, "Java Script Kiddie", "Web Exploitation", "", "reconstruction PNG + QR", f,
             "Comme Java Script Kiddie 2 mais la cle fait 16 caracteres (un chiffre 0-9 par colonne). "
             "La signature PNG (8 premiers octets) et l'en-tete IHDR (8 suivants) determinent 14 des "
             "16 shifters ; les 2 colonnes ambigues sont resolues en essayant les combinaisons jusqu'a "
             "un PNG decodable. Le PNG est un **QR code** avec le flag.")
