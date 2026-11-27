import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{b1663r_15_b3773r_d84eb852}"
st, b = cy.req("GET", "/api/challenges/319/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 319, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"319 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(319, "x-sixty-what", "Binary Exploitation", "", "ret2win x64 (offset 72)", f,
             "Binaire x64 non-PIE avec `gets(buf[64])` et une fonction `flag()` a 0x401236. L'offset "
             "vers l'adresse de retour est **64 + 8 = 72**. Il faut sauter a **0x40123b** (juste apres "
             "le `push rbp`) et non au debut de la fonction, sinon le desalignement de pile provoque un "
             "segfault dans `movaps`.")
