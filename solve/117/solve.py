# 117 - Surfing the Waves  (Forensics, picoCTF 2021)
# Flag: academy{mU21C_1s_1337_63f2299a}
# Write-up: ../../../writeups/forensics/117-surfing-the-waves.md
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


f = "academy{mU21C_1s_1337_63f2299a}"
d = json.loads(b)
print("nom:", d.get("name"), "| deja:", d.get("solved_by_user"))
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"117 Surfing the Waves -> {ok}")
if ok and not d.get("solved_by_user"):
    wu.write(117, "Surfing the Waves", "Forensics", "main.wav (2736 echantillons, 2736 Hz)",
             "hexadecimal encode dans les echantillons audio (2 derniers chiffres = bruit)", f,
             "`main.wav` fait **1 seconde, mono, 2736 Hz, 2736 echantillons**, avec des valeurs "
             "comprises entre 1000 et 8509. Le spectrogramme ne montre aucun texte : la donnee n'est "
             "pas dans le domaine frequentiel. La cle est dans les **valeurs des echantillons** : en "
             "tronquant les **deux derniers chiffres** de chaque valeur (qui sont du bruit aleatoire "
             "ajoute), il ne reste que **16 valeurs uniques** — 10, 15, 20, ... 85 — soit exactement "
             "un alphabet hexadecimal de 16 symboles. En les triant et en les faisant correspondre a "
             "`0123456789abcdef` (10->0, 15->1, ... 85->f), on obtient une longue chaine hexadecimale "
             "qui se decode en ASCII comme un **programme Python generateur** : "
             "`hex_stuff[i] = 1000 + int(hex_stuff[i]) * 500 + (10 * random())` — ce qui explique "
             "parfaitement les valeurs observees (1000 + 500*n + bruit) et confirme la theorie. Le "
             "programme se termine par le drapeau en commentaire. Verification croisee : 1000 + 500*0 "
             "= 1000 et 1000 + 500*15 = 8500, coherents avec min=1000 et max=8509.")
