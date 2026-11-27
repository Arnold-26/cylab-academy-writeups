# 50 - seed-sPRiNG  (Binary Exploitation, picoCTF 2019)
# Flag: academy{pseudo_random_number_generator_not_so_random_d1009105}
# Write-up: ../../../writeups/binary-exploitation/50-seed-spring.md
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


f = "academy{pseudo_random_number_generator_not_so_random_d1009105}"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"50 seed-sPRiNG (deja={already}) -> {ok}")
if ok and not already:
    wu.write(50, "seed-sPRiNG", "Binary Exploitation", "nc chatelaine.cylabacademy.net 44519",
             "graine srand(time(0)) previsible -> 30 valeurs devinees", f,
             "Le binaire 32 bits `seed_spring` initialise le generateur avec `srand(time(0))` (visible a "
             "0x13a1 puis 0x13b3) et fait jouer **30 niveaux**, chacun comparant l'entree a "
             "`rand() & 0xf` (0x13ee puis `and eax,0xf`). Comme la graine est l'horodatage en secondes, on "
             "rejoue le meme `rand()` de la glibc en local (`ctypes.CDLL('libc.so.6')` avec "
             "`libc.srand(seed)` puis `libc.rand() & 0xf`) et on envoie les 30 valeurs d'un coup : scanf lit "
             "le flux en tampon, donc tout passe. La graine est l'heure courante (delta 0 suffit). Il faut "
             "attendre ~4 secondes avant de lire, sinon on ne recoit que les premiers prompts et on croit a "
             "tort que les valeurs sont fausses. Apres les 30 niveaux, `get_flag()` execute `cat flag.txt`.")
