import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{p0p_r0p_4nd_dr0p_1t_57265dd1560e0e20}"
st, b = cy.req("GET", "/api/challenges/89/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 89, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"89 Guessing Game 2 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(89, "Guessing Game 2", "Binary Exploitation", "nc xebec.cylabacademy.net <port>",
             "format string (fuite canari + lecture GOT) + ret2libc 32 bits", f,
             "Le binaire 32 bits `guessing-game-2-vuln` a deux bugs. (1) `get_random()` renvoie `rand` "
             "**sans parentheses**, donc l'adresse libc de la fonction ; comme le programme est en 32 bits, "
             "cette adresse devient negative en `long` et `ans = (adresse % 4096) + 1` tombe dans "
             "[-4094, 1]. La reponse est **-2623** (trouvee en envoyant les 4094 valeurs negatives d'un "
             "seul coup : `fgets` consomme le flux tamponne, et le `-2624` qui suit apparait comme nom du "
             "gagnant). (2) `win()` fait `gets(winner)` dans un buffer de 512 a `ebp-0x20c` puis "
             "`printf(winner)` : **format string**. Le canari est a `ebp-0xc`, soit la **position 135** de "
             "la pile de format string (le buffer commence en position 7 : `(135-7)*4 = 512`). Attention, "
             "une chaine de plus de 512 octets ecrase deja le canari — d'ou l'echec des scans larges. "
             "La chaine de format permet aussi une **lecture arbitraire** : on envoie "
             "`p32(atol@got)` + `%7$s`, `gets` acceptant les octets bruts, et on lit l'adresse libc "
             "resolue. Le fingerprint (atol 0x3d2e0, printf 0x57120, gets 0x75e20, fgets 0x74980, "
             "puts 0x768d0) identifie **glibc 2.39 (libc6-i386_2.39-0ubuntu8.9)** via libc.rip, avec "
             "`system` = 0x4f8e0 et `/bin/sh` = 0x1bcde8. `main` rebouclant, on enchaine : fuite atol, "
             "fuite canari (`%135$p`), puis debordement `512*A + canari + 8 octets de locales + saved ebp "
             "+ system + ret + /bin/sh`. Le piege final : il y a **8 octets de variables locales entre le "
             "canari et le saved ebp** (le retour est a 528, pas a 520).")
