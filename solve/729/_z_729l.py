import sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cands = [
    "academy{i5_tH15_s3cr3T_k3Y_5tbax3er}",
    "academy{n0T_F0uNd_s3cr3T_K3y_34rd76s1}",
    "academy{n0T_F0uNd_s3cr3T_k3Y_c5d243edq}",
    "academy{tH15_lS_n0T_s3cr3T_k3Y_vbr1qa43}",
    "academy{tH15_lS_n0T_f!@G_5rwdf731q}",
]
cy = CyLab(delay=1.2)
cy.login()
st, b = cy.req("GET", "/api/challenges/729/")
already = json.loads(b).get("solved_by_user")
print("deja resolu:", already)
good = None
for c in cands:
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 729, "flag": c})
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print(f"  {c[:60]:62} -> {ok}")
    if ok:
        good = c
        break
    time.sleep(1)
print("FLAG RETENU:", good)
if good and not already:
    wu.write(729, "Sql Map1", "Web Exploitation", "http://xebec.cylabacademy.net:<port>/vuln.php",
             "SQL injection UNION sur SQLite (2 colonnes) apres login", good,
             "Application PHP avec inscription et login, puis une zone authentifiee : une recherche "
             "`vuln.php?q=` qui concatene directement l'entree dans une requete. Le SGBD est **SQLite**, "
             "ce que revele le message d'erreur (`SQLite3::query(): Unable to prepare statement`). "
             "La requete a **2 colonnes** : `' UNION SELECT 1,2-- -` renvoie des lignes, alors que 1 ou "
             "3 colonnes produisent une erreur. Le schema se lit dans `sqlite_master` : "
             "`users(id, username, password)` et `flags(id, key, value)`. Le dump complet de `flags` "
             "montre une majorite de leurres explicites (`n0T_F0uNd`, `lS_n0T`) et une valeur "
             "distincte pour `flag3` ; c'est celle-la qui est acceptee. Les mots de passe des "
             "utilisateurs sont des **MD5** (pratique de hachage obsolete evoquee par l'enonce), mais "
             "l'injection suffit a lire le drapeau sans casser de hash.")
