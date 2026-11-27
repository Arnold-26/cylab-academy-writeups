import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{3332fad6faebb3893d505e8880e32abe}"
st, b = cy.req("GET", "/api/challenges/746/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 746, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"746 tea-cash (deja={already}) -> {ok}")
if ok and not already:
    wu.write(746, "tea-cash", "Binary Exploitation", "nc chatelaine.cylabacademy.net <port>",
             "traversee de la tcache free list (LIFO) + chunks contigus", f,
             "Le programme (source fournie) alloue 6 chunks de `CHUNK_SIZE = 0x80` via `malloc`, place "
             "le contenu de flag.txt a `chunks[5] + 8` (`FLAG_OFFSET = sizeof(void*)`), affiche "
             "`tcache head -> %p` (= `chunks[0]`), puis libere les chunks dans l'ordre **5, 4, 3, 2, "
             "1, 0**. La tcache est une pile LIFO : apres ces free, la chaine est "
             "`chunks[0] -> chunks[1] -> chunk[2] -> chunks[3] -> chunks[4] -> chunks[5] -> NULL`. Le "
             "programme demande ensuite 6 adresses et lit a chaque fois le pointeur `next` en memoire "
             "pour avancer, en verifiant que la valeur correspond a un chunk connu ou NULL. Il suffit "
             "donc de fournir les 6 adresses dans l'ordre. On n'en connait qu'une (la tete), mais un "
             "malloc de 0x80 donne un chunk de taille utile 0x90, et les 6 allocations sont "
             "consecutives : `chunks[i] = head + i*0x90`. Envoyer `head`, `head+0x90`, ..., "
             "`head+5*0x90` produit « Correct traversal! » et affiche le flag. Pas besoin de libc : "
             "l'arithmetique sur les offsets suffit (ce qui confirme que le libc n'utilise pas le "
             "safe-linking, sinon les pointeurs `next` seraient masques).")
