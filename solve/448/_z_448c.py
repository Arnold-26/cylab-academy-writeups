import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{f0rm47_57r?_f0rm47_m3m_18b9edd8}"
st, b = cy.req("GET", "/api/challenges/448/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 448, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"448 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(448, "format string 2", "Binary Exploitation", "", "format string write (%hn)", f,
             "Binaire non-PIE avec `printf(buf)` et un global `sus` (0x404048) valant 0x21737573. "
             "Il faut le rendre egal a 0x67616c66. Le buffer est en **position 14** dans les arguments "
             "du printf. On ecrit 0x6761 a l'adresse 0x40404a puis 0x6c66 a 0x404048 via deux `%hn` "
             "en ordre croissant (`%26465c%18$hn%1285c%19$hn` + padding + adresses).")
