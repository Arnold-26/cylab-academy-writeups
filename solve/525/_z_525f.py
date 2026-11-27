import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{0v3rfl0w_c0mm4nd_d0e158ad}"
st, b = cy.req("GET", "/api/challenges/525/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 525, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"525 Input Injection 1 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(525, "Input Injection 1", "Binary Exploitation", "nc chatelaine.cylabacademy.net <port>",
             "stack overflow : ecrasement du buffer de commande passe a system()", f,
             "Programme 64 bits non-PIE sans canary (source fournie, 31 lignes). `main` lit un nom de "
             "200 octets et appelle `fun(name, \"uname\")`. Dans `fun`, la pile est : `char c[10]` a "
             "`rbp-0xa` et `char buffer[10]` a `rbp-0x14` — donc `buffer` est 10 octets SOUS `c`, et les "
             "deux sont exactement adjacents (`rbp-0x14 + 10 = rbp-0xa`). Le code fait "
             "`strcpy(c, cmd)` puis `strcpy(buffer, name)` : le second `strcpy` deborde du buffer et "
             "ecrase `c`, qui contenait \"uname\", AVANT l'appel `system(c)`. Il suffit donc d'envoyer "
             "**10 octets de remplissage suivis de la commande** : `\"A\"*10 + \"cat *\"`. Le programme "
             "affiche `Goodbye, AAAAAAAAAAcat *!` puis `system` execute notre commande et affiche le "
             "flag. Aucune adresse a calculer, pas de ROP : la primitive est directement un "
             "« argument injection » par debordement de pile. Le flag est dans le repertoire courant, "
             "`cat *` suffit sans connaitre le nom du fichier.")
