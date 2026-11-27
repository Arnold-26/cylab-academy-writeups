# 386 - Virtual Machine 1  (Reverse Engineering, picoCTF 2023)
# Flag: academy{m0r3_g34r5_3g4d_c3dc2830}
# Write-up: ../../../writeups/reverse-engineering/386-virtual-machine-1.md
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


f = "academy{m0r3_g34r5_3g4d_c3dc2830}"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"386 VM1 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(386, "Virtual Machine 1", "Reverse Engineering", "nc xebec.cylabacademy.net 12383",
             "ratio compose d'engrenages (7*191*7)", f,
             "Meme principe que VM0 mais avec un **train d'engrenages bevel a 3 etages** : le ratio "
             "compose vaut 7 x 191 x 7 = **9359**. Le service demande « If the input to the machine is "
             "<n>, what is the output? » : il faut multiplier l'entier fourni par 9359 et renvoyer le "
             "resultat. Le modele `.dae` contient les pieces LEGO (3647=8 dents, 3648b=16, 3649/4019=24, "
             "32270=12, plus les axes 3704/3707/32073/4519) ; la difficulte est de ne pas oublier "
             "l'etage intermediaire cache derriere le carter, sinon on multiplie deux ratios au lieu de trois.")
