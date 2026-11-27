# 706 - Forensics Git 1  (Forensics, picoCTF 2026)
# Flag: academy{g17_r3m3mb3r5_d4ddf904}
# Write-up: ../../../writeups/forensics/706-forensics-git-1.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{g17_r3m3mb3r5_d4ddf904}"
st, b = cy.req("GET", "/api/challenges/706/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 706, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"706 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(706, "Forensics Git 1", "Forensics", "", "objet git supprime (historique)", f,
             "Image disque de 1 Go (racine a l'offset 1140736). Le depot git contient 5 objets : "
             "un blob avec le flag, un commit « Add flag » qui le reference, puis un commit "
             "« Remove flag » qui le supprime de l'arbre. Le blob reste dans `.git/objects` : en "
             "decompressant les objets zlib extraits via `fls`/`icat`, on retrouve le flag.")
