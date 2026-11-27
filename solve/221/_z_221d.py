import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "picoCTF{y0uv3_3sc4p3d_th3_m4ze...f0r_n0w-hYkq2D9PmrA5GpEq}"
st, b = cy.req("GET", "/api/challenges/221/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 221, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"221 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(221, "MATRIX", "Reverse Engineering", "nc mars.cylabacademy.net 31259", "VM custom + BFS labyrinthe", f,
             "Le binaire est une **VM a pile** faite main : un dispatch sur un octet d'opcode, avec deux piles "
             "(principale + alt), des sauts conditionnels, et GETCHAR/PUTCHAR. Le bytecode embarque un "
             "**labyrinthe** : `#` murs, `^` gagne de la vie, `v` en perd, `$` sortie, et 5 checkpoints "
             "verifient que le compteur de vie >= 5. Le chemin le plus court geometriquement echoue car il "
             "saute les `^`. Chemin valide de 63 coups : "
             "`rrrrrlrlrlrlrllddddddlddrrddrrrrdddrruuuruuuuuuurrddddddddlddrd`. Le flag n'est pas dans le "
             "binaire : il est lu depuis `flag.txt` sur le serveur, donc il faut l'envoyer a l'instance nc.")
