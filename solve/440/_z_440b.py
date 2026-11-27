import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{now_thats_free_real_estate_95cc82ff}"
st, b = cy.req("GET", "/api/challenges/440/")
d = json.loads(b)
print("nom:", d.get("name"), "| deja:", d.get("solved_by_user"))
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 440, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"440 heap 3 -> {ok}")
if ok and not d.get("solved_by_user"):
    wu.write(440, "heap 3", "Binary Exploitation", "nc xebec.cylabacademy.net <port>",
             "use-after-free : free(x) sans remise a NULL + reallocation du meme chunk", f,
             "Source fournie. Le struct `object` contient `char a[10]; char b[10]; char c[10]; "
             "char flag[5]` (35 octets), et `x = malloc(sizeof(object))` recoit \"bico\" dans `flag`. "
             "La faille est un **use-after-free** : l'option 5 appelle `free(x)` **sans mettre x a "
             "NULL**, et l'option 2 fait `malloc(size)` puis `scanf(\"%s\", alloc)` sans borne. En "
             "demandant la meme taille (35), le malloc retourne **le chunk qui vient d'etre libere** "
             "(LIFO de la tcache), donc la zone de `alloc` est exactement celle de l'ancien `x`. "
             "`check_win()` teste `strcmp(x->flag, \"pico\")` : comme `flag` est a l'offset 30 du "
             "struct, on envoie `30 octets de remplissage + \"pico\"`. L'option 3 (« Print x->flag ») "
             "confirme la reussite en affichant `x = pico`, puis l'option 4 affiche le drapeau. "
             "Verification utile : la meme sequence sans le padding affiche `x = AAAA...` et echoue, "
             "ce qui prouve que le decalage de 30 octets est bien celui du champ `flag`.")
