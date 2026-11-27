import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{brut4_f0rc4_cf2e78d0}"
st, b = cy.req("GET", "/api/challenges/520/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 520, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"520 Crack the Gate 1 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(520, "Crack the Gate 1", "Web Exploitation", "http://chatelaine.cylabacademy.net:<port>/",
             "commentaire HTML ROT13 -> en-tete X-Dev-Access: yes", f,
             "Portail de login Express (Node). Le formulaire n'a pas d'attribut `action` : le JS de la page "
             "appelle `fetch('/login', {...})` en JSON. La faille est dans le **code source HTML** : un "
             "commentaire encode en **ROT13** traine dans la page — "
             "`<!-- ABGR: Wnpx - grzcbenel olcnff: hfr urnqre \"K-Qri-Npprff: lrf\" -->` — qui se decode en "
             "« NOTE: Jack - temporary bypass: use header X-Dev-Access: yes », suivi d'un second "
             "commentaire « Remove before pushing to production! ». Il suffit d'envoyer "
             "`POST /login` avec `X-Dev-Access: yes` (sans meme un mot de passe valide) pour obtenir "
             "`{\"success\":true,...,\"flag\":\"academy{...}\"}`. Sans l'en-tete la reponse est "
             "`{\"success\":false,\"error\":\"Unauthorized access.\"}` — le contraste confirme la "
             "backdoor. Lecon : toujours lire le source HTML, les commentaires sont envoyes a tous les "
             "navigateurs.")
