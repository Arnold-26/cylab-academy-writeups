# 221 - MATRIX  (Reverse Engineering, picoMini by redpwn)
# Flag: picoCTF{y0uv3_3sc4p3d_th3_m4ze...f0r_n0w-hYkq2D9PmrA5GpEq}
# Write-up: ../../../writeups/reverse-engineering/221-matrix.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import wu

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""


f = "picoCTF{y0uv3_3sc4p3d_th3_m4ze...f0r_n0w-hYkq2D9PmrA5GpEq}"
already = json.loads(b).get("solved_by_user")
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
