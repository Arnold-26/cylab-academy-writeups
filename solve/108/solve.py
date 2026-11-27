# 108 - Startup Company  (Web Exploitation, picoCTF 2021)
# Flag: academy{1_c4nn0t_s33_y0u_66b27680}
# Write-up: ../../../writeups/web-exploitation/108-startup-company.md
# This is the script that produced the flag; historical variants are in archive/.
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


f = "academy{1_c4nn0t_s33_y0u_66b27680}"
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("108 Startup Company ->", ok)
if ok:
    wu.write(108, "Startup Company", "Web Exploitation", "http://chatelaine.cylabacademy.net:<port>/",
             "injection SQLite dans le champ moneys (concatenation + commentaire)", f,
             "Application **PHP/Apache** (`index.php`, `register.php`, `contribute.php`) qui affiche ses "
             "warnings PHP. Particularite : l'inscription utilise les champs `user`/`pass` alors que "
             "`index.php` lit `username`/`password` ; une fois les bons noms envoyes, inscription et login "
             "fonctionnent. Le formulaire de don a un **captcha a usage unique** : il faut recharger "
             "`index.php` avant chaque contribution sinon « Invalid captcha » (piege qui fait echouer les "
             "tests en serie). Le champ `moneys` est **injectable en SQLite** : `1' UNION SELECT 1--` "
             "renvoie `SQLite3::query(): Unable to prepare statement: 1, near \"UNION\": syntax error` "
             "avec le chemin `/var/www/html/contribute.php`. Le message d'erreur revele la fin de la "
             "requete : `' WHERE nameuser='`, donc notre entree est dans un **literal de chaine** et il "
             "faut **commenter la suite**. Payload final : "
             "`moneys='||(SELECT GROUP_CONCAT(wordpass) FROM startup_users)-- -` avec un captcha frais ; "
             "la page affiche alors tous les mots de passe dans le solde, dont celui de "
             "`the_real_flag` qui contient le drapeau.")
