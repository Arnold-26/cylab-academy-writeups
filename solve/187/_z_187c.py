import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{d0ubl3_j30p4rdy_7d637ab1}"
st, b = cy.req("GET", "/api/challenges/187/")
d = json.loads(b)
print("nom:", d.get("name"), "| deja:", d.get("solved_by_user"))
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 187, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"187 Unsubscriptions Are Free -> {ok}")
if ok and not d.get("solved_by_user"):
    wu.write(187, "Unsubscriptions Are Free", "Binary Exploitation",
             "nc xebec.cylabacademy.net <port>",
             "use-after-free : free(user) sans NULL puis reallocation du meme chunk", f,
             "Binaire 32 bits non-PIE. La structure `cmd { uintptr_t (*whatToDo)(); char *username; }` "
             "est allouee avec `malloc(sizeof(user))` — donc **8 octets seulement** au lieu de 16, et "
             "surtout `i()` fait `free(user)` **sans remettre le pointeur a NULL**. La boucle principale "
             "appelle ensuite `doProcess(user)` qui execute `(*user->whatToDo)()`. L'option `l` "
             "(`leaveMessage`) alloue exactement `malloc(8)` : apres le free, la tcache rend **le meme "
             "chunk**, et `read(0, msg, 8)` ecrit donc a l'emplacement de `whatToDo`. Exploit en trois "
             "etapes : (1) `I` puis `Y` pour liberer `user` ; (2) `L` puis envoyer "
             "`p32(0x08049266)` = adresse de `hahaexploitgobrrr` (binaire non-PIE, donc fixe ; "
             "l'option `S` fuit d'ailleurs cette adresse avec `printf(\"%p\")`) ; (3) la boucle appelle "
             "`doProcess(user)` et saute sur `hahaexploitgobrrr`, qui affiche le drapeau. Piege "
             "classique : il faut synchroniser sur les invites (« (Y/N)? » et « try anyways: ») et "
             "envoyer les 4 octets de l'adresse SANS newline, car `read` ne les attend pas.")
