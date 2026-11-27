import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "b21866bc4c80386c60f652271399ef0b"
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 133, "flag": f})
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("133 Binary Gauntlet 3 ->", ok)
if ok:
    wu.write(133, "Binary Gauntlet 3", "Binary Exploitation",
             "nc xebec.cylabacademy.net <port>",
             "ret2one_gadget : format string pour fuiter libc, strcpy interdit une chaine ROP", f,
             "Binaire 64 bits **non-PIE** avec **NX actif** (`GNU_STACK RW`), libc-2.27 fournie. "
             "`main` : `malloc`, `fgets` puis **`printf(heap)`** (format string : le premier `fgets` est "
             "affiche tel quel, ce qui permet de fuiter la pile), deuxieme `fgets`, puis "
             "`strcpy(rbp-0x70, heap)` — offset de l'adresse de retour **0x70 + 8 = 120**. Offsets "
             "releves dans la libc : `__libc_start_main` 0x21ba0, `system` 0x4f420, `/bin/sh` 0x1b3d88, "
             "`pop rdi; ret` 0x2164f (scan de `5f c3` dans `.text`). **Fuite exploitable :** sur 60 `%p`, "
             "la valeur d'indice 18 vaut `…c87` mod 0x1000 = `__libc_start_main+231` (0x21c87) ; "
             "attention, ces adresses commencent par `0x7xxx` et non `0x7f`, mon premier filtre de plage "
             "les excluait. **Piege decisif :** `strcpy` s'arrete au premier octet NUL, donc une chaine "
             "ROP de plusieurs adresses 64 bits est **impossible** (chaque adresse a 2 octets hauts "
             "nuls) — il faut un **one-gadget**. `base + 0x4f2c5` a fonctionne du premier coup "
             "(payload `A*0x70 + B*8 + p64(base+0x4f2c5)`), et le shell a permis `cat flag.txt`. "
             "Astuce plateforme : les liens de fichiers n'apparaissent dans la description que "
             "**juste apres le PUT**.")
