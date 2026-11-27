import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{n3v3r_z1p_2_h1d3_2f899900}"
st, b = cy.req("GET", "/api/challenges/507/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 507, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"507 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(507, "DISKO 3", "Forensics", "", "FAT32 + flag.gz", f,
             "L'image est un systeme **FAT32** (pas de table de partitions). Un `fls -r` revele "
             "`/var/log/flag.gz` (inode 522628) ; `icat` l'extrait et `gunzip` donne le flag.")
