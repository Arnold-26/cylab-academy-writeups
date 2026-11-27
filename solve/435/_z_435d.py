import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{and_down_the_road_we_go_67bc01d6}"
st, b = cy.req("GET", "/api/challenges/435/")
d = json.loads(b)
print("nom:", d.get("name"), "| deja:", d.get("solved_by_user"))
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 435, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"435 heap 2 -> {ok}")
if ok and not d.get("solved_by_user"):
    wu.write(435, "heap 2", "Binary Exploitation", "nc chatelaine.cylabacademy.net <port>",
             "debordement de tas : ecrasement d'un pointeur de fonction sur le tas", f,
             "Source fournie (92 lignes). `init()` alloue `input_data = malloc(5)` puis `x = malloc(5)` "
             "— deux chunks **adjacents** de taille utile 0x20 chacun. `write_buffer()` fait "
             "`scanf(\"%s\", input_data)` **sans borne**, donc on deborde du premier chunk dans le "
             "second, qui contient le pointeur de fonction. `check_win()` execute "
             "`movsxd rcx, DWORD PTR [x]` puis `jmp rcx` : il lit un **entier 32 bits** a l'adresse x "
             "et saute dessus. Le binaire est **non-PIE** (`ET_EXEC`), donc `win` a une adresse fixe : "
             "0x4011a0. Payload = 32 octets de remplissage + `p32(0x4011a0)`, envoye a l'option 2, puis "
             "option 4. Le menu « Print Heap » (option 1) confirme la disposition : "
             "input_data=0x37b82b0 et x=0x37b82d0, soit exactement 0x20 d'ecart, ce qui valide le "
             "padding. Les octets nuls de l'adresse passent car `%s` ne s'arrete qu'aux espaces.")
