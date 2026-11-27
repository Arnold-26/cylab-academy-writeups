# 387 - VNE  (Binary Exploitation, picoCTF 2023)
# Flag: academy{Power_t0_man!pul4t3_3nv_72f8870f}
# Write-up: ../../../writeups/binary-exploitation/387-vne.md
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


f = "academy{Power_t0_man!pul4t3_3nv_72f8870f}"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"387 VNE (deja={already}) -> {ok}")
if ok and not already:
    wu.write(387, "VNE", "Binary Exploitation", "ssh ctf-player@xebec.cylabacademy.net -p <port>",
             "injection de commande dans la variable d'environnement SECRET_DIR", f,
             "Acces SSH (compte `ctf-player`). Le binaire `bin` est **setuid root** "
             "(`-rwsr-xr-x root root`) et affiche `Error: SECRET_DIR environment variable is not set` "
             "quand on le lance nu. `strings` montre qu'il utilise `system()` et le message "
             "`Error: system() call returned non-zero value`. Avec `SECRET_DIR=/root` il liste "
             "effectivement le contenu de /root (on y voit `flag.txt`), ce qui confirme l'execution "
             "privilegiee. La variable est ensuite concaténee telle quelle dans la commande passee a "
             "`system()`, donc on injecte avec un point-virgule : "
             "`SECRET_DIR=\"/root; id\" ./bin` affiche `uid=0(root)`, et "
             "`SECRET_DIR=\"/root; cat /root/flag.txt\" ./bin` affiche le drapeau. Autre preuve que "
             "l'injection est bien dans l'environnement et pas dans un argument : le message affiche la "
             "valeur brute avant execution (« Listing the content of /root; id as root »).")
