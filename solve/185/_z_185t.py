import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{h0p3fully_u_t0ok_th3_r1ght_xp4th_b61f3d39}"
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 185, "flag": f})
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("185 X marks the spot ->", ok)
if ok:
    wu.write(185, "X marks the spot", "Web Exploitation", "http://xebec.cylabacademy.net:<port>/",
             "injection XPath aveugle via contains()", f,
             "Page de login servie par **Flask/Werkzeug 3.0.1 sur Python 3.12.3**, formulaire `name`/`pass` "
             "en POST sur `/`. L'indice « I don't use any of those regular old unsafe query "
             "languages! » signifie que ce n'est **pas du SQL** : c'est du **XPath**. Deux faux "
             "diagnostics a corriger : (1) j'ai d'abord teste du **NoSQL** (`name[$ne]`, `name[$gt]`, "
             "`name[$regex]`, en form-urlencoded ET en JSON) — toutes ces requetes renvoient la page "
             "initiale (3398 octets), le corps JSON etant meme totalement ignore ; (2) toute valeur "
             "contenant une **guillemet simple** provoquait un **500** avec mes payloads SQL, ce qui "
             "confirmait un point d'injection mais pas la syntaxe. La bonne injection est aveugle et "
             "utilise XPath : `name = ' or //*[contains(.,\"PREFIXE\")] or 'x'='` avec `pass=asdf`. "
             "**Piege de la sentinelle** : le writeup d'origine parle de « You're on the right track », "
             "mais cette instance repond **« You're on the right path. »** (3757 octets) contre "
             "« Login failure. » (3741 octets) — mes premiers tests etaient donc tous faux negatifs "
             "alors que l'injection marchait deja. Extraction caractere par caractere (alphabet "
             "a-z 0-9 _ } - ! A-Z), en parallele (4 threads) avec verification par `contains()` du "
             "prefixe accumule. Attention : trop de requetes fait tomber l'instance "
             "(ConnectionError) — il faut la relancer par PUT et espacer. Resultat : "
             "`academy{h0p3fully_u_t0ok_th3_r1ght_xp4th_b61f3d39}`.")
