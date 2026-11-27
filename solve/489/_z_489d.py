import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{Co-@utH0r_Of_Sy5tem_b!n@riEs_bf204e06}"
st, b = cy.req("GET", "/api/challenges/489/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 489, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"489 hash-only-2 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(489, "hash-only-2", "Binary Exploitation", "ssh ctf-player@chatelaine.cylabacademy.net -p <port>",
             "contournement de rbash par invocation explicite de bash + PATH hijack", f,
             "Meme cible que hash-only-1 (un `flaghasher` setuid root qui appelle `md5sum` sur "
             "/root/flag.txt), mais la session SSH est cette fois un **rbash** (shell restreint) : `PATH` "
             "est en lecture seule, les redirections sont refusees et les `/` sont interdits dans les noms "
             "de commandes, ce qui bloque le detournement direct. Le contournement est simple : `rbash` "
             "n'applique ses restrictions qu'au shell invoque sous ce nom. En passant une commande "
             "explicite `bash -c \"...\"` a ssh, on obtient un bash **non restreint** (uid=1001, PATH "
             "modifiable). On recree alors le faux `md5sum` dans $HOME, on le met en tete de PATH et on "
             "lance `flaghasher` : il s'execute en euid root (id renvoie uid=0) et affiche le flag. "
             "`flaghasher` seul se contente de renvoyer l'empreinte MD5 "
             "7e43bc81db2ecf3d242aa1574a92f8c3.")
