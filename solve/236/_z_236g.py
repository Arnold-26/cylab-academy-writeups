import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{succ3ss_@u7h3nt1c@710n_3fa1c59d}"
st, b = cy.req("GET", "/api/challenges/236/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 236, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"236 JAuth (deja={already}) -> {ok}")
if ok and not already:
    wu.write(236, "JAuth", "Web Exploitation", "http://xebec.cylabacademy.net:<port>/",
             "JWT alg=none : signature vide acceptee", f,
             "Portail bancaire Node avec authentification par **JWT** stocke dans le cookie `token`. On "
             "se connecte avec le compte fourni `test` / `Test123!` (formulaire POST sur `/auth`, "
             "redirection vers `/private`) et on recupere un token HS256 dont le payload est "
             "`{\"auth\":1795549596539,\"agent\":\"curl/8.20.0\",\"role\":\"user\",\"iat\":...}`. "
             "La bibliotheque JWT accepte l'algorithme **`none`** : il suffit de reecrire l'en-tete en "
             "`{\"typ\":\"JWT\",\"alg\":\"none\"}` et de changer `role` en `admin`, en laissant la "
             "signature VIDE (le token se termine par un point, sans troisieme segment). Le serveur ne "
             "verifie alors aucune signature et sert `/private` en tant qu'admin, ce qui affiche le flag. "
             "C'est l'une des vulnerabilites classiques des librairies JWT mal configurees : toujours "
             "valider explicitement l'algorithme attendu et interdire `none`.")
