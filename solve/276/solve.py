# 276 - Keygenme  (Reverse Engineering, picoCTF 2022)
# Flag: academy{br1ng_y0ur_0wn_k3y_bb724f88}
# Write-up: ../../../writeups/reverse-engineering/276-keygenme.md
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


f = "academy{br1ng_y0ur_0wn_k3y_bb724f88}"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"276 Keygenme (deja={already}) -> {ok}")
if ok and not already:
    wu.write(276, "Keygenme", "Reverse Engineering", "", "extraction de la chaine attendue par gdb", f,
             "`keygenme` (ELF 64 PIE stripped) demande une licence. La fonction de verification (0x1209) "
             "construit **le flag attendu sur la pile** : une serie de `movabs` partiellement chevauchants "
             "ecrit `academy{H` a [rbp-0x90], `br1ng_y0H` a +8, `g_y0ur_0H` a +12 (ce qui ecrase et recolle "
             "en `br1ng_y0ur_0`), puis `wn_k3y_` a +20, donnant `academy{br1ng_y0ur_0wn_k3y_`. Ensuite "
             "l'entree est hashee en MD5, convertie en hexa par `sprintf(\"%02x\")`, et une partie de cet "
             "hexadecimal complete le flag. La comparaison finale (0x1442) est INLINE (boucle sur 36 "
             "caracteres), donc les hooks LD_PRELOAD sur strcmp/memcmp ne declenchent rien. Il faut un "
             "**breakpoint gdb a 0x1442** (base PIE 0x555555554000 avec ASLR desactive, et entree de 36 "
             "caracteres sinon la fonction sort avant par un controle de longueur) puis `x/s $rbp-0x30` : "
             "la chaine complete y est en clair.")
