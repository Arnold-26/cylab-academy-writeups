import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{g17_r35cu3_16ac6bf3}"
st, b = cy.req("GET", "/api/challenges/707/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 707, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"707 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(707, "Forensics Git 2", "Forensics", "", "objets git decompresses", f,
             "Image disque de 1 Go (3 partitions ; la racine est a l'offset 1140736). Un depot git se "
             "trouve dans `/home/ctf-player/Code/killer-chat-app/.git`. J'ai extrait les objets via "
             "`fls`/`icat` puis decompresse chaque objet zlib : le flag est dans l'un des blobs.")
