import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{ChEeSy8b0897b1}"
st, b = cy.req("GET", "/api/challenges/473/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 473, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"473 Guess My Cheese 1 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(473, "Guess My Cheese (Part 1)", "Cryptography", "nc chatelaine.cylabacademy.net <port>",
             "chiffrement affine + oracle d'encryption (CHEDDAR) -> 312 cles", f,
             "Le service affiche un fromage secret chiffre et propose deux commandes : `g` (deviner) et "
             "`e` (chiffrer). C'est un **chiffrement affine** E(x) = (a*x + b) mod 26 sur A-Z, avec une "
             "cle **aleatoire par session** et seulement 3 tentatives. Le piege : l'oracle n'accepte que "
             "de VRAIS noms de fromages (envoyer `aaaaaaaaaa` consomme une tentative pour rien) et il "
             "ignore silencieusement tout caractere hors A-Z. Il faut donc envoyer un fromage connu, par "
             "exemple **CHEDDAR**, ce qui donne une paire clair/chiffre ; deux lettres suffisent pour "
             "resoudre le systeme (2a+b et 7a+b modulo 26). On peut aussi brute-forcer les 312 cles "
             "(12 valeurs de a inversibles x 26 valeurs de b) : c'est instantane et sans risque d'erreur "
             "de calcul. Avec (a,b) on dechiffre le fromage secret par D(y) = a^-1 * (y - b) mod 26, puis "
             "on l'envoie via `g`. Les noms sont volontairement exotiques (« they might look different "
             "from cheeses you're used to ») : ici le secret etait `TOMAI`, et la soumission a fonctionne "
             "en majuscules.")
