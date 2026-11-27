# 14 - droids1  (Reverse Engineering, picoCTF 2019)
# Flag: academy{pining.for.the.fjords}
# Write-up: ../../../writeups/reverse-engineering/14-droids1.md
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


f = "academy{pining.for.the.fjords}"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"14 droids1 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(14, "droids1", "Reverse Engineering", "", "XOR répétitif clé=mot de passe dans la lib native", f,
             "Le mot de passe est la ressource `password` = **`opossum`**. `fenugreek(input)` appelle "
             "`nutmeg(input)` (validation) puis `anise(input)`, qui fait "
             "`unscramble(data@0x1a3e, 0x1e, strdup(input), strlen(input))` : **la cle du XOR est "
             "l'input lui-meme**. Avec `opossum` on obtient `academy{pining.for.the.fjords}`.")
