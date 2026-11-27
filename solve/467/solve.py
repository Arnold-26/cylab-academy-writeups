# 467 - Apriti sesamo  (Web Exploitation, picoCTF 2025)
# Flag: academy{w3Ll_d3sErV3d_Ch4mp_4b876558}
# Write-up: ../../../writeups/web-exploitation/467-apriti-sesamo.md
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


f = "academy{w3Ll_d3sErV3d_Ch4mp_4b876558}"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"467 Apriti sesamo (deja={already}) -> {ok}")
if ok and not already:
    wu.write(467, "Apriti sesamo", "Web Exploitation", "http://chatelaine.cylabacademy.net:<port>/impossibleLogin.php",
             "PHP type juggling : tableaux passes a sha1() -> null === null", f,
             "Application PHP avec une page de login « impossible a hacker ». Le formulaire poste sur "
             "`impossibleLogin.php` avec deux champs, `username` et `pwd`. Le writeup indique que le "
             "backup Emacs `impossibleLogin.php~` divulgue la source, laquelle compare "
             "`sha1($username) === sha1($pwd)` en **egalite stricte**. La faille n'est pas le magic "
             "hash (inutile avec `===`) mais le **type juggling** : si on envoie des TABLEAUX au lieu "
             "de chaines, `sha1()` leve un warning et retourne **null** pour les deux appels, donc "
             "`null === null` est vrai et le login passe sans aucun identifiant valide. En pratique il "
             "suffit de poster `username[]=a&pwd[]=b` (noms de champs suffixes de crochets). La reponse "
             "affiche directement le flag. Lecon : ne jamais laisser une fonction de hash recevoir un "
             "type non verifie ; valider `is_string()` avant.")
