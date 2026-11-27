import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
cands = [
    "academy{d0Nt_r0ll_yoUr_0wN_aES}",
    "picoCTF{d0Nt_r0ll_yoUr_0wN_aES}",
    "academy{d0Nt_r0ll_yoUr_0wN_crypt0}",
    "academy{d0Nt_r0ll_yoUr_0wN_crypt0_60d3}",
]
for cand in cands:
    st, b = cy.req("GET", "/api/challenges/76/")
    already = json.loads(b).get("solved_by_user")
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 76, "flag": cand})
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print(f"76 {cand} -> {ok}")
    if ok:
        if not already:
            wu.write(76, "AES-ABC", "Cryptography", "", "inversion du chainage ABC (addition mod 2^128)", cand,
                     "Le mode custom ajoute le bloc chiffre precedent au bloc courant (mod 2^128). On "
                     "inverse en soustrayant : `n_curr = (curr - prev) mod 2^128` en parcourant les blocs. "
                     "Le resultat est toujours du **AES-ECB** (cle inconnue), mais ECB preserve les "
                     "motifs : les zones uniformes de l'image donnent des blocs identiques, donc le texte "
                     "du flag reste lisible dans le PPM.")
        break
