import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{sy5teM_b!n@riEs_4r3_5c@red_0f_yoU_8e21ab6c}"
st, b = cy.req("GET", "/api/challenges/487/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 487, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"487 hash-only-1 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(487, "hash-only-1", "Binary Exploitation", "ssh ctf-player@chatelaine.cylabacademy.net -p <port>",
             "PATH hijack sur un binaire setuid qui appelle md5sum", f,
             "Le challenge donne un acces SSH (`ctf-player`, mot de passe fourni) sur une machine ou se "
             "trouve `flaghasher`, un binaire **setuid root** (-rwsr-xr-x root). Il affiche l'empreinte "
             "MD5 de `/root/flag.txt` via un appel du type `system(\"md5sum /root/flag.txt\")`. Un binaire "
             "setuid herite de l'environnement de l'appelant, donc `PATH` est detournable : on ecrit un "
             "faux `md5sum` dans son home (`cat /root/flag.txt`), on met `$HOME` en tete de `PATH`, puis "
             "on lance `./flaghasher`. Le faux binaire s'execute avec l'euid root (`id` renvoie uid=0) et "
             "affiche le contenu du fichier flag. C'est l'illustration classique du message de l'enonce : "
             "« system binaries are sacred » — un chemin absolu ou la securisation de PATH l'aurait evite.")
