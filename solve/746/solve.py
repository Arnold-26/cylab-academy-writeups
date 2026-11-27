# 746 - tea-cash  (Binary Exploitation, picoCTF 2026)
# Flag: academy{3332fad6faebb3893d505e8880e32abe}
# Write-up: ../../../writeups/binary-exploitation/746-tea-cash.md
# Script exact utilise pour produire le flag.
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


f = "academy{3332fad6faebb3893d505e8880e32abe}"
already = json.loads(b).get("solved_by_user")
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
