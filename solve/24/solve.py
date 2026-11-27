# 24 - Forky  (Reverse Engineering, picoCTF 2019)
# Flag: academy{-721750240}
# Write-up: ../../../writeups/reverse-engineering/24-forky.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
cands = ["academy{3573217056}", "3573217056", "academy{-721750240}", "-721750240"]
for cand in cands:
    st, b = cy.req("GET", "/api/challenges/24/")
    already = json.loads(b).get("solved_by_user")
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 24, "flag": cand})
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print(f"24 {cand} -> {ok}")
    if ok:
        if not already:
            wu.write(24, "Forky", "Reverse Engineering", "", "analyse de fork + mmap partage", cand,
                     "Le programme `mmap` une zone **partagee** initialisee a 0x3B9ACA00 (1000000000), "
                     "puis `fork()` 4 fois (16 processus). Chaque processus ajoute 0x499602D2 "
                     "(1234567890) a la valeur partagee et passe le resultat a `doNothing`. Le dernier "
                     "appel recoit la valeur apres les 16 additions : 1000000000 + 16*1234567890 "
                     "mod 2^32 = 3573217056.")
        break
