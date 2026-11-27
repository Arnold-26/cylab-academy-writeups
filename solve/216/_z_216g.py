import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "picoCTF{c0ntr0ll3d_clutt3r_1n_my_buff3r}"
st, b = cy.req("GET", "/api/challenges/216/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 216, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"216 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(216, "clutter-overflow", "Binary Exploitation", "", "buffer overflow -> variable = 0xdeadbeef", f,
             "Le service lit notre entree dans un buffer de 256 octets suivi d'une variable `code` "
             "(8 octets) qu'il compare a `0xdeadbeef`. L'offset est **264** (determine en envoyant "
             "`A`*n + `B`*8 et en lisant la valeur affichee : elle passe a 0x4242424242424242 a n=264). "
             "On envoie donc 264 octets + `p64(0xdeadbeef)`.")
