import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

a = 965270072
# func1: a>100 -> func2(a+100)
x = a + 100
# func2: x>499 -> func5(x+13)
x = x + 13
# func5 -> func8(x) = x+2
x = x + 2
print("resultat:", x, "hex:", format(x & 0xFFFFFFFF, "08x"))
f = "academy{%s}" % format(x & 0xFFFFFFFF, "08x")
cy = CyLab(delay=1.2)
cy.login()
st, b = cy.req("GET", "/api/challenges/183/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 183, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"183 ARMssembly 4 (deja={already}) -> {ok}  ({f})")
if ok and not already:
    wu.write(183, "ARMssembly 4", "Reverse Engineering", "", "interpretation a la main d'un .S ARM", f,
             "Le source ARM64 `chall_4.S` : `main` appelle `func1(atoi(argv[1]))` avec a=965270072. "
             "`func1` : si a>100 -> `func2(a+100)` sinon `func3(a)`. `func2` : si x>499 -> "
             "`func5(x+13)` sinon `func4(x-86)`. `func5` -> `func8(x)` qui fait `x+2`. Chaine : "
             "965270072 -> 965270172 -> 965270185 -> 965270187 = 0x39885dab. Les autres branches "
             "(`func3`/`func4`/`func6`/`func7`) ne sont jamais prises avec cette entree.")
