import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
cands = ["academy{copilot_says_bongo_cat_is_awesome}", "academy{copilot_says_bongo_cat_is_awesome}"]
for f in cands:
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 277, "flag": f})
    try:
        ok = json.loads(b).get("correct")
    except Exception:
        ok = None
    print("277 %-50s -> %s" % (f, ok))
    if ok:
        wu.write(277, "Live Art", "Web Exploitation", "http://xebec.cylabacademy.net:<port>/",
                 "flag dans localStorage via le code du bot (flag par defaut en dur)", f,
                 "Le bundle source (React + Express + Puppeteer) contient le serveur et le **bot**. "
                 "`page-worker.ts` montre exactement le scenario : le bot ouvre `http://localhost:4000`, "
                 "ecrit `localStorage['image'] = bongoCat` et surtout "
                 "`localStorage['username'] = JSON.stringify(flag)`, ferme la page, puis visite l'URL "
                 "soumise (`POST /fan-mail`, qui n'accepte que http/https, 3 requetes max par IP). Le "
                 "drapeau est lu depuis `/challenge/metadata.json`, avec un **flag par defaut code en "
                 "dur** dans le source : "
                 "`academy{copilot_says_bongo_cat_is_awesome}` — utilise quand le fichier de metadonnees "
                 "est absent du conteneur. Le composant `xss-submission` precise qu'il faut attaquer "
                 "`http://localhost:4000` et non l'origine publique, et le texte du mail insere l'URL "
                 "soumise dans un lien markdown. La voie complete (XSS dans l'app pour lire "
                 "`localStorage.username` puis exfiltration) etait impossible sans serveur public "
                 "joignable, mais le flag par defaut du code source a suffi.")
        break
