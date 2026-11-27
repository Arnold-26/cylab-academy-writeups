import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{pYth0nn_libraryH!j@CK!n9_15d0fa80}"
st, b = cy.req("GET", "/api/challenges/352/")
d = json.loads(b)
print("nom:", d.get("name"), "| deja:", d.get("solved_by_user"))
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 352, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"352 hijacking -> {ok}")
if ok and not d.get("solved_by_user"):
    wu.write(352, "hijacking", "Binary Exploitation", "ssh academy@chatelaine.cylabacademy.net -p <port>",
             "Python library hijacking : module base64 malveillant importe par un script sudo root", f,
             "Acces SSH (compte `academy`). `sudo -l` revele une regle NOPASSWD : "
             "`(root) /usr/bin/python3 /home/academy/.server.py`. Le script est la propriete de root et "
             "contient `import base64`, `import os`, `import socket`, puis "
             "`os.system(\"ping -c 1 \" + ip)`. `sudo` impose `secure_path`, donc detourner `ping` par "
             "PATH ne fonctionne pas — mais Python cherche les modules dans **`sys.path[0]`, le dossier "
             "du script**, c'est-a-dire `/home/academy`, qui appartient a l'utilisateur. On cree donc "
             "`/home/academy/base64.py` contenant `import os; os.system(...)`, et l'execution via "
             "`sudo /usr/bin/python3 /home/academy/.server.py` importe CE module au lieu de celui de la "
             "stdlib : le code s'execute en **uid=0** (verifie avec `id`). Le flag n'etait pas dans "
             "`/root/flag.txt` mais dans **`/root/.flag.txt`** (fichier cache), trouve avec "
             "`find / -iname \"*flag*\"`. Lecon : un script sudo qui importe un module Python depuis un "
             "dossier inscriptible est une escalation de privileges directe.")
