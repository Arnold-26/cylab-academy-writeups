import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{d3bug_f0r_th3_Win_0x100_411bc019}"
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 429, "flag": f})
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("429 WinAntiDbg0x100 ->", ok)
if ok:
    wu.write(429, "WinAntiDbg0x100", "Reverse Engineering", "WinAntiDbg0x100.exe (zip, mdp academy)",
             "anti-debug Windows : patch de IsDebuggerPresent + debogueur ctypes maison", f,
             "Executable Windows 32 bits protege par zip, mot de passe **`academy`** (donne dans la "
             "description complete de l'instance — pas le classique `infected`). Le programme refuse de "
             "demarrer sans debogueur : « To start the challenge, you'll need to first launch this "
             "program using a debugger! ». J'ai donc ecrit un **mini-debogueur en Python/ctypes** : "
             "`CreateProcessW` avec `DEBUG_ONLY_THIS_PROCESS`, boucle `WaitForDebugEvent` / "
             "`ContinueDebugEvent`, et lecture des `OutputDebugString` via `ReadProcessMemory`. "
             "**Piege majeur :** dans `DEBUG_EVENT`, l'union commence a l'offset **16** en 64 bits "
             "(alignement), pas 12 — avec 12 on lit des pointeurs fantomes (`0xa382c800000000`) et des "
             "longueurs nulles. Le debogueur revele alors : « Level 1 … talent for growing a 'patch' of "
             "roses! » puis « The debugger was detected ». Les contournements par ecriture memoire "
             "echouent : `PEB.BeingDebugged` (PEB+2) ne suffit pas, ajouter `NtGlobalFlag` (PEB+0xBC) "
             "coupe toute sortie, et patcher les flags du tas (`heap+0x70/0x74`) **tue le processus**. "
             "La bonne solution est de **patcher le binaire** : `pefile` donne l'IAT de "
             "`IsDebuggerPresent` (0x403014) et deux sites d'appel `ff 15 14 30 40 00` aux offsets "
             "**0x9fc** et **0x119e**, remplaces par `31 c0 90 90 90 90` (`xor eax,eax` + nops) : le "
             "test renvoie 0 et le drapeau s'affiche.")
