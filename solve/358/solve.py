# 358 - More SQLi  (Web Exploitation, picoCTF 2023)
# Flag: academy{G3tting_5QL_1nJ3c7I0N_l1k3_y0u_sh0ulD_b5ff84c8}
# Write-up: ../../../writeups/web-exploitation/358-more-sqli.md
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


f = "academy{G3tting_5QL_1nJ3c7I0N_l1k3_y0u_sh0ulD_b5ff84c8}"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"358 More SQLi (deja={already}) -> {ok}")
if ok and not already:
    wu.write(358, "More SQLi", "Web Exploitation", "http://chatelaine.cylabacademy.net:<port>/",
             "SQL injection UNION-based (SQLite) : bypass login puis extraction", f,
             "Application PHP 8.3 avec SQLite. La requete de login est "
             "`SELECT id FROM users WHERE password = '<pw>' AND username = '<user>'` — **le mot de passe "
             "est evalue en premier**, et l'application affiche la requete en cas d'erreur 500. Trois "
             "etapes : (1) contourner le login avec `password = ' OR 1=1 LIMIT 1-- ` — le `LIMIT 1` est "
             "indispensable car sans lui la requete renvoie plusieurs lignes et provoque une erreur 500 ; "
             "le formulaire repond alors 302 vers `welcome.php`. (2) Sur `welcome.php` il y a une "
             "recherche d'agences a 3 colonnes (City, Address, Phone) ; on enumere le schema par "
             "`' UNION SELECT sql,null,null FROM sqlite_master;--`, ce qui revele les tables `hints`, "
             "`more_table (id, flag)`, `offices` et `users`. (3) On lit le flag par "
             "`' UNION SELECT flag,null,null FROM more_table;--`. Les cookies de session PHP sont "
             "necessaires entre les deux etapes. Note pratique : ce site n'est joignable que depuis WSL "
             "(curl), le Python Windows echoue en resolution DNS.")
