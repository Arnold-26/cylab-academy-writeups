# 487 - hash-only-1  (Binary Exploitation, picoCTF 2025)
# Flag: academy{sy5teM_b!n@riEs_4r3_5c@red_0f_yoU_8e21ab6c}
# Write-up: ../../../writeups/binary-exploitation/487-hash-only-1.md
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


f = "academy{sy5teM_b!n@riEs_4r3_5c@red_0f_yoU_8e21ab6c}"
already = json.loads(b).get("solved_by_user")
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
