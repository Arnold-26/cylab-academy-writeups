import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{Power_t0_man!pul4t3_3nv_72f8870f}"
st, b = cy.req("GET", "/api/challenges/387/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 387, "flag": f})
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
