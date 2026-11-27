# 298 - SideChannel  (Forensics, picoCTF 2022)
# Flag: academy{t1m1ng_4tt4ck_55dcfc0f}
# Write-up: ../../../writeups/forensics/298-sidechannel.md
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


f = "academy{t1m1ng_4tt4ck_55dcfc0f}"
already = json.loads(b).get("solved_by_user")
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
