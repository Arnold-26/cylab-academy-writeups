import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{not.particularly.silly}"
st, b = cy.req("GET", "/api/challenges/17/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 17, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"17 droids4 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(17, "droids4", "Reverse Engineering", "", "emulation du StringBuilder + XOR natif", f,
             "`FlagstaffHill.getFlag` reconstruit le mot de passe avec quatre `StringBuilder` initialises "
             "a `aaa` (ace/jack/queen/king) et des `setCharAt` qui AJOUTENT des constantes : ace +0x13/+0x12, "
             "jack +7/0/+1, queen +0/+0xb/+0xf, king +0xe/+0x14/+0xf, puis concatene "
             "`queen+jack+ace+king` -> **`alphabetsoup`** (sans espace). Le flag vient de "
             "`pepper()` = XOR repetitif des donnees a 0x1aa0 (31 octets) avec la cle = le mot de passe. "
             "Piege : avec `alphabet soup` (avec espace) on obtient `academy{` correct sur 8 octets puis "
             "du bruit, ce qui fait croire a un mauvais chemin.")
