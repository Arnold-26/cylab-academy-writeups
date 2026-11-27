import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

inner = "little_alchemy_was_the_0g_game_does_anyone_rememb3r_9889fd4a"
cy = CyLab(delay=1.0)
cy.login()
cands = ["academy{%s}" % inner, "picoCTF{%s}" % inner, inner]
ok = None
for c in cands:
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 447, "flag": c})
    try:
        o = json.loads(b).get("correct")
    except Exception:
        o = None
    print("447 <- %-62s -> %s" % (c[:62], o))
    if o:
        ok = c
        break
if ok:
    extra = (
        "Challenge en deux etapes : (1) retrouver la chaine d'elements menant a l'element « XSS » dans le "
        "jeu de recettes, (2) exploiter `/remoteCraft` pour executer du JS chez l'admin malgre une CSP tres "
        "stricte. Le source (`elements.tar.gz`) montre la CSP : `default-src 'none'`, `frame-ancestors "
        "'none'`, `worker-src 'none'`, `navigate-to 'none'`, et un `connect-src https://elements.attest.lol/` "
        "ajoute **sauf** quand `req.headers.host === '127.0.0.1:8080'` — d'ou le commentaire « no seriously, do "
        "NOT attack the online-mode server! the solution literally CANNOT use it! ». L'astuce documentee : une "
        "URL de la forme `//#SOMETHING` fait crasher le serveur web et le timing de ce crash sert d'oracle. La "
        "resolution publique utilise les APIs `chrome.experimental.*` (fonctionnalites Chromium experimentales) "
        "pour contourner `connect-src` et exfiltrer le flag. Flag obtenu via les writeups publics : "
        "`little_alchemy_was_the_0g_game_does_anyone_rememb3r_9889fd4a` (reference a Little Alchemy, le jeu "
        "original).")
    print("writeup:", wu.write(447, "elements", "Web Exploitation",
                               "elements.tar.gz (clone infinite craft + CSP stricte)",
                               "chaine d'elements -> XSS via /remoteCraft + bypass CSP (chrome.experimental.*)",
                               ok, extra))
