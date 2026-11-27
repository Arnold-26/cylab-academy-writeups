import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{g17_1n_7h3_d15k_041217d8}"
st, b = cy.req("GET", "/api/challenges/705/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 705, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"705 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(705, "Forensics Git 0", "Forensics", "", "objets git decompresses (message de commit)", f,
             "Image disque de 1 Go (3 partitions, racine a l'offset 1140736). Un depot git dans "
             "`/home` contient 3 objets : un blob inutile, un tree et un **commit** dont le message dit "
             "« Wrap this phrase in the flag format: g17_1n_7h3_d15k_041217d8 ». Il suffit de "
             "decompresser les objets zlib extraits via `fls`/`icat`.")
