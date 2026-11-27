# 306 - stack cache  (Binary Exploitation, picoCTF 2022)
# Flag: academy{Cle4N_uP_M3m0rY_0761b234}
# Write-up: ../../../writeups/binary-exploitation/306-stack-cache.md
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


f = "academy{Cle4N_uP_M3m0rY_0761b234}"
ok = json.loads(b).get("correct") if b.startswith("{") else None
print("306 stack cache ->", ok)
if ok:
    wu.write(306, "stack cache", "Binary Exploitation", "nc chatelaine.cylabacademy.net <port>",
             "ret2win + UnderConstruction : le flag reste sur la pile et fuit via les %p non initialises", f,
             "Binaire **32 bits, statiquement lie, non-PIE** (clang-12, sans optimisation). `vuln()` "
             "utilise `gets(buf)` avec `char buf[10]` place en **ebp-0xa**, donc l'offset de retour est "
             "de **14 octets**. `win()` (0x08049810) lit `flag.txt` avec `fgets(buf,0x40,fp)` dans une "
             "locale (ebp-0x40) mais **ne l'affiche jamais** : le drapeau reste donc « en cache » sur la "
             "pile, car C ne nettoie pas la frame au retour. `UnderConstruction()` (0x08049890) imprime "
             "**10 `%p` sur des locales qu'elle n'initialise jamais** : en l'appelant juste apres `win`, "
             "ces locales relisent la zone de pile ou le drapeau vient d'etre ecrit. Chaine : "
             "`b'A'*14 + p32(win) + p32(UnderConstruction) + p32(main)`. Les 8 pointeurs non triviaux, "
             "relus en little-endian, donnent les morceaux `acad`, `emy{`, `Cle4`, `N_uP`, `_M3m`, "
             "`0rY_`, `0761`, `b234` ; en les remettant dans l'ordre on obtient le drapeau. Pieges : "
             "les 2 premiers `%p` sont des adresses de code inutiles, et l'ordre des mots est inverse "
             "de l'ordre d'affichage.")
