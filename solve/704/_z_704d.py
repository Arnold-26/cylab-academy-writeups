import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{d3l_d0n7_h1d3_w3ll_9748d144}"
st, b = cy.req("GET", "/api/challenges/704/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 704, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"704 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(704, "DISKO 4", "Forensics", "", "fichier supprime dans FAT32", f,
             "Image FAT32. `fls -r -d` revele un fichier **supprime** `log/dont-delete.gz` "
             "(inode 532021). `icat` le recupere et `gunzip` donne le flag.")
