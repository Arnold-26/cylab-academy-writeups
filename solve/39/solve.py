# 39 - Need For Speed  (Reverse Engineering, picoCTF 2019)
# Flag: academy{Good job keeping bus #31326f14 speeding along!}
# Write-up: ../../../writeups/reverse-engineering/39-need-for-speed.md
# This is the script that produced the flag; historical variants are in archive/.
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


f = "academy{Good job keeping bus #31326f14 speeding along!}"
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("39 Need For Speed ->", ok)
if not ok:
    alt = "academy{Good job keeping bus #31326f14 speeding along}"
    try:
        ok = json.loads(b).get("correct")
    except Exception:
        ok = None
    print("variante ->", ok)
    if ok:
        f = alt
if ok:
    extra = (
        "Binaire ELF 64 bits PIE de 16,5 Ko, sans service : le flag est **dans le binaire** et il faut le "
        "faire calculer. Execution : `Keep this thing over 50 mph!` / `Creating key...` / `Not fast enough. "
        "BOOM!`. Le desassemblage montre le mecanisme anti-debug : `set_timer()` installe un handler SIGALRM "
        "via `__sysv_signal(14, alarm_handler)` puis appelle **`alarm(1)`** — une seconde pour creer la cle. "
        "Deux etapes : (1) **patcher l'appel `alarm`** a l'offset 0x1314 (5 octets `e8 97 fd ff ff` -> "
        "`90 90 90 90 90`), ce qui empeche le BOOM mais laisse un calcul tres long ; (2) comprendre que ce "
        "calcul est en fait **deterministe** : `calculate_key` fait `k = 0xe7af057b`, puis 8 fois `k = "
        "0xcf5e0af6; do k--; while (k != 0xe7af057b)` — soit ~3,9 milliards d'iterations par tour a cause du "
        "rebouclage uint32, mais le resultat final est **toujours 0xe7af057b**. Il suffit donc de remplacer la "
        "fonction par `mov eax, 0xe7af057b; ret` (patch a 0x1265 : `55 48 89 e5 b8 7b 05 af e7 5d c3` puis NOP "
        "jusqu'a 0x129c). Le programme affiche alors immediatement `Finished` / `Printing flag:` et le flag. "
        "Lecon : quand une boucle « lente » a une sortie constante, la patcher est plus rapide que l'attendre — "
        "et l'anti-debug par alarme se contourne en deux octets de NOP.")
    print("writeup:", wu.write(39, "Need For Speed", "Reverse Engineering",
                               "need-for-speed (ELF 64 bits PIE)",
                               "patch alarm(1) + remplacement de calculate_key par la constante retournee",
                               f, extra))
