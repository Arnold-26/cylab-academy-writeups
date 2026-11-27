import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{gamer_m0d3_enabled_77d1c3e4}"
st, b = cy.req("GET", "/api/challenges/345/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 345, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"345 babygame01 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(345, "babygame01", "Binary Exploitation", "nc chatelaine.cylabacademy.net <port>",
             "ecriture hors-limites sur l'octet 'has flag' adjacent a la carte", f,
             "Jeu de labyrinthe 32 bits : la structure joueur est a `ebp-0xaa4` (x, y, has_flag) "
             "et la carte a `ebp-0xa98`, donc la carte commence 12 octets APRES le joueur et l'octet "
             "« a le drapeau » se trouve a `map[-4]`. Les deplacements ne verifient pas les bornes : "
             "`move_player` ecrit la tuile du joueur (0x70, 'p') a `map[x*90 + y]`. En allant en "
             "**(0,-4)** on ecrase donc l'octet du drapeau avec 0x70 (non nul). La condition de "
             "victoire dans `main` teste `player.x == 29 && player.y == 89` puis `if (byte[ebp-0xa9c])` "
             "avant d'appeler `win()`. Sequence : `w*4` (x=0), `a*8` (y=-4) pour le drapeau, puis "
             "`s*29` et `d*93` pour atteindre (29,89). Le service distant passe par un PTY : il faut "
             "envoyer la sequence **suivie d'un saut de ligne**, sinon le programme reste bloque en "
             "attente et rien ne s'execute (le PTY renvoie seulement l'echo).")
