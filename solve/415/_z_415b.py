import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
cands = [
    "academy{cert!f1Ed_iNd!4n_s0rrY_3nDian_5b37ea4e}",
    "academy{cert!f1Ed_iNd!4n_s0rrY_3nDian}",
]
for f in cands:
    st, b = cy.req("GET", "/api/challenges/415/")
    already = json.loads(b).get("solved_by_user")
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 415, "flag": f})
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print(f"415 {f} -> {ok}")
    if ok:
        if not already:
            wu.write(415, "endianness-v2", "Forensics", "", "inversion d'endianness par blocs de 4", f,
                     "Le fichier provient d'un systeme 32 bits qui a organise les octets a l'envers : en "
                     "inversant chaque groupe de **4 octets**, on obtient un JPEG valide (`ffd8ffe0`...). "
                     "L'image affiche le flag.")
        break
