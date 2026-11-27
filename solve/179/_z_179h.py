import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{1_l0v3_sm4sh_st4cking_a768fad93c216715}"
st, b = cy.req("GET", "/api/challenges/179/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 179, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"179 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(179, "Here's a LIBC", "Binary Exploitation", "", "ret2libc en 2 etapes (leak puts)", f,
             "`do_stuff` fait `scanf(\"%[^\\n]\", buf)` sur `rbp-0x80` (offset 136 vers l'adresse de "
             "retour). Le format est **`%[^\\n]` et non `%s`** : les octets `0x09` passent, donc le "
             "gadget `pop rdi ; ret` (0x400913, qui contient un 0x09) est utilisable. Etape 1 : "
             "`pop rdi ; puts@got ; puts@plt ; do_stuff` -> fuite de l'adresse de puts. Etape 2 : "
             "`ret ; pop rdi ; binsh ; system` (le `ret` supplementaire corrige l'alignement 16 octets). "
             "Note : `convert_case` transforme les 100 premiers octets (padding) mais pas l'adresse de "
             "retour, qui commence a l'offset 136.")
