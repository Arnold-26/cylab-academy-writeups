# 183 - ARMssembly 4  (Reverse Engineering, picoCTF 2021)
# Flag: academy{3988daab}
# Write-up: ../../../writeups/reverse-engineering/183-armssembly-4.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import wu

a = 965270072
# func1: a>100 -> func2(a+100)
x = a + 100
# func2: x>499 -> func5(x+13)
x = x + 13
# func5 -> func8(x) = x+2

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

x = x + 2
print("resultat:", x, "hex:", format(x & 0xFFFFFFFF, "08x"))
f = "academy{%s}" % format(x & 0xFFFFFFFF, "08x")
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"183 ARMssembly 4 (deja={already}) -> {ok}  ({f})")
if ok and not already:
    wu.write(183, "ARMssembly 4", "Reverse Engineering", "", "interpretation a la main d'un .S ARM", f,
             "Le source ARM64 `chall_4.S` : `main` appelle `func1(atoi(argv[1]))` avec a=965270072. "
             "`func1` : si a>100 -> `func2(a+100)` sinon `func3(a)`. `func2` : si x>499 -> "
             "`func5(x+13)` sinon `func4(x-86)`. `func5` -> `func8(x)` qui fait `x+2`. Chaine : "
             "965270072 -> 965270172 -> 965270185 -> 965270187 = 0x39885dab. Les autres branches "
             "(`func3`/`func4`/`func6`/`func7`) ne sont jamais prises avec cette entree.")
