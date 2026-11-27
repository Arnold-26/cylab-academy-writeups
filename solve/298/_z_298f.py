import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{t1m1ng_4tt4ck_55dcfc0f}"
st, b = cy.req("GET", "/api/challenges/298/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 298, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"298 SideChannel (deja={already}) -> {ok}")
if ok and not already:
    wu.write(298, "SideChannel", "Forensics", "nc xebec.cylabacademy.net 48223",
             "attaque temporelle sur un PIN a 8 chiffres", f,
             "`pin_checker` (ELF 32 bits) verifie un PIN a 8 chiffres et **compare caractere par caractere "
             "avec un delai**, ce qui cree un oracle temporel. En local (pas de bruit reseau), on determine "
             "le PIN position par position : pour chacun des 8 chiffres, on essaie les 10 possibilites en "
             "gardant le prefixe deja trouve et en completant par des zeros, on mesure le temps median de "
             "3 executions, et on garde le chiffre le plus lent (le plus de caracteres corrects = le plus de "
             "delais accumules). Temps mesures : 385 ms -> 523 -> 743 -> 1177 -> 1079 -> 1279 -> 1351 -> "
             "1451 ms, PIN = **48390513**, que le binaire accepte (« Access granted »). Le PIN se rentre "
             "ensuite sur le serveur maitre, qui renvoie le flag.")
