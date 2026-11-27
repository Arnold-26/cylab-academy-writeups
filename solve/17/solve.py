# 17 - droids4  (Reverse Engineering, picoCTF 2019)
# Flag: academy{not.particularly.silly}
# Write-up: ../../../writeups/reverse-engineering/17-droids4.md
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


f = "academy{not.particularly.silly}"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"17 droids4 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(17, "droids4", "Reverse Engineering", "", "emulation du StringBuilder + XOR natif", f,
             "`FlagstaffHill.getFlag` reconstruit le mot de passe avec quatre `StringBuilder` initialises "
             "a `aaa` (ace/jack/queen/king) et des `setCharAt` qui AJOUTENT des constantes : ace +0x13/+0x12, "
             "jack +7/0/+1, queen +0/+0xb/+0xf, king +0xe/+0x14/+0xf, puis concatene "
             "`queen+jack+ace+king` -> **`alphabetsoup`** (sans espace). Le flag vient de "
             "`pepper()` = XOR repetitif des donnees a 0x1aa0 (31 octets) avec la cle = le mot de passe. "
             "Piege : avec `alphabet soup` (avec espace) on obtient `academy{` correct sur 8 octets puis "
             "du bruit, ce qui fait croire a un mauvais chemin.")
