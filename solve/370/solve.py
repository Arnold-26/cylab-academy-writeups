# 370 - Ready Gladiator 2  (Reverse Engineering, picoCTF 2023)
# Flag: academy{d3m0n_3xpung3r_36e6efa4}
# Write-up: ../../../writeups/reverse-engineering/370-ready-gladiator-2.md
# Script exact utilise pour produire le flag.
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


f = "academy{d3m0n_3xpung3r_36e6efa4}"
d = json.loads(b)
print("nom:", d.get("name"), "| deja:", d.get("solved_by_user"))
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"370 Ready Gladiator 2 -> {ok}")
if ok and not d.get("solved_by_user"):
    wu.write(370, "Ready Gladiator 2", "Reverse Engineering", "nc xebec.cylabacademy.net <port>",
             "CoreWars : warrior Gnat qui bat l'Imp 100/100", f,
             "Le service lance un combat **CoreWars** (RedCode) : il faut fournir un warrior qui bat "
             "« The Imp » (`mov 0, 1`) sur 100 rounds. Le warrior soumis est lu sur stdin jusqu'a "
             "`end`. Apres avoir teste sans succes des strategies naives, le writeup donne la solution "
             "fiable : **Gnat** (`gnat  mov -1, <-2` puis `jmp gnat, <-3`), un warrior qui se recopie "
             "en decalage et finit par ecraser l'Imp. Resultat verifie : « Rounds: 100 / Warrior 1 "
             "wins: 100 / Warrior 2 wins: 0 / Ties: 0 », puis le flag. Envoi : "
             "`nc <host> <port> < gnat.red`. Detail : le fichier doit finir par `end`, sinon le "
             "service attend encore.")
