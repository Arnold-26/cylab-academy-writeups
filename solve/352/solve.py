# 352 - hijacking  (Binary Exploitation, picoCTF 2023)
# Flag: academy{pYth0nn_libraryH!j@CK!n9_15d0fa80}
# Write-up: ../../../writeups/binary-exploitation/352-hijacking.md
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


f = "academy{pYth0nn_libraryH!j@CK!n9_15d0fa80}"
d = json.loads(b)
print("nom:", d.get("name"), "| deja:", d.get("solved_by_user"))
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
