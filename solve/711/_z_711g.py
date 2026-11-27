import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{th4ts_s0_N0t_TRU3_f5e1dd98}"
st, b = cy.req("GET", "/api/challenges/711/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 711, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"711 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(711, "no. no. that's Not TRUe", "Cryptography", "", "attaque en treillis NTRU (fpylll)", f,
             "NTRU avec des parametres minuscules (N=48, p=3, q=509). On construit le treillis NTRU "
             "`[I H ; 0 qI]` (H circulante de h), on le reduit avec **LLL puis BKZ(40)** : les "
             "vecteurs courts donnent f (ternaire, norme^2=35). On inverse f mod p par pivot de Gauss "
             "pour obtenir f_p_inv, puis `m = f_p_inv * (f*c mod q) mod p` redonne les bits du message.")
