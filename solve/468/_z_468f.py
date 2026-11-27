import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{UseSecure#$_Random@j3n3r@T0rs02d049c1}"
st, b = cy.req("GET", "/api/challenges/468/")
d = json.loads(b)
print("nom:", d.get("name"), "| deja:", d.get("solved_by_user"))
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 468, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"468 Chronohack -> {ok}")
if ok and not d.get("solved_by_user"):
    wu.write(468, "Chronohack", "Reverse Engineering", "nc xebec.cylabacademy.net <port>",
             "seed de PRNG base sur time.time()*1000 : brute force temporel", f,
             "Le generateur fourni (`token_generator.py`, 45 lignes) fait "
             "`random.seed(int(time.time() * 1000))` puis 20 fois `random.choice(alphabet)` : le token "
             "est **entierement determine par l'horodatage en millisecondes** au demarrage du "
             "programme. Le service accepte 50 tentatives par connexion, donc chaque connexion permet "
             "de tester 50 seeds consecutifs. Deux points mesures par l'experience : (1) le token est "
             "regenere a chaque connexion (un nouveau processus est lance) — verifie en consommant 50 "
             "tentatives puis en rouvrant une connexion, qui redemarre bien a zero ; (2) le decalage "
             "entre l'horloge locale et la date de demarrage du programme est de l'ordre de la centaine "
             "de millisecondes (trouve a **+100 ms**). Le facteur decisif a ete le **pipelining** : "
             "envoyer les 50 candidats d'un seul coup et lire la reponse en bloc, au lieu d'attendre le "
             "prompt entre chaque essai — le scan complet de +/-10 s est passe de plusieurs heures a "
             "2,5 minutes. Une fois le bon seed trouve, la reponse « Congratulations! » est suivie du "
             "contenu de /flag.txt.")
