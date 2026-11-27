# 180 - Super Serial  (Web Exploitation, picoCTF 2021)
# Flag: academy{1_c4nn0t_s33_y0u_cf804c42}
# Write-up: ../../../writeups/web-exploitation/180-super-serial.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{1_c4nn0t_s33_y0u_cf804c42}"
st, b = cy.req("GET", "/api/challenges/180/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 180, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"180 Super Serial (deja={already}) -> {ok}")
if ok and not already:
    wu.write(180, "Super Serial", "Web Exploitation", "http://xebec.cylabacademy.net:<port>/",
             "PHP object injection via cookie deserialise + lecture de fichier", f,
             "Le site est une app PHP avec login. `robots.txt` revele `Disallow: /admin.phps`, et la "
             "divulgation de source via l'extension `.phps` expose tout le code : `index.php` serialise "
             "un objet `permissions` dans le cookie `login` (base64 + urlencode), `authentication.php` "
             "teste `$perm->is_admin()`, et `cookie.php` definit deux classes — `permissions` "
             "(requetes SQLite parametrees, donc pas d'injection SQL) et surtout **`access_log`** dont "
             "`__toString()` appelle `read_log()` -> `file_get_contents($this->log_file)`. Le cookie "
             "etant deserialise sans controle, on forge un objet `access_log` avec "
             "`log_file = \"../flag\"` : `O:10:\"access_log\":1:{s:8:\"log_file\";s:7:\"../flag\";}` "
             "encode en base64 puis urlencode. `authentication.php` declenche `__toString()` sur cet "
             "objet et affiche le contenu du fichier. Le chemin exact importe : `/flag` et "
             "`/flag.txt` echouent (« No such file »), c'est `../flag` qui marche car le flag est un "
             "niveau au-dessus de /var/www/html.")
