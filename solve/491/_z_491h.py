import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{p13_5h0u1dn'7_134k_afc2dccb}"
st, b = cy.req("GET", "/api/challenges/491/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 491, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"491 PIE TIME 2 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(491, "PIE TIME 2", "Binary Exploitation", "nc xebec.cylabacademy.net <port>",
             "fuite PIE par format string + saut arbitraire", f,
             "Le programme (source fournie) lit un nom dans un buffer de 64 octets, l'affiche avec "
             "`printf(buffer)` — **format string** — puis demande une adresse (`scanf(\"%lx\")`) et "
             "l'appelle directement via un pointeur de fonction. Il y a une fonction `win()` qui ouvre "
             "et imprime flag.txt. La solution tient donc en deux temps dans la MEME session (chaque "
             "connexion lance un nouveau processus, donc une nouvelle base PIE) : on envoie `%25$p`, qui "
             "fuit l'adresse de `main` (base + 0x1418), on calcule `base = leak - 0x1418`, puis "
             "`win = base + 0x1376`, et on l'envoie comme adresse de saut. `win()` affiche alors le flag. "
             "Le piege : les premiers `%N$p` ne donnent que des valeurs de pile et une adresse libc ; il "
             "faut chercher plus loin (position 25) pour tomber sur l'adresse PIE. Un gestionnaire de "
             "SIGSEGV intercepte les mauvaises adresses et affiche « Segfault Occurred ».")
