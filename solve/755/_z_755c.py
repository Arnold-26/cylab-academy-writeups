import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{3ch0_s3rv1c3_br34k5_7fcd4fec}"
st, b = cy.req("GET", "/api/challenges/755/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 755, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"755 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(755, "Echo Escape 1", "Binary Exploitation", "", "read() overflow (offset 40)", f,
             "`char buf[32]` puis `read(0, buf, 128)` : debordement de 96 octets. Binaire x86-64 "
             "non-PIE, `win()` a 0x401256 lit et affiche le flag. Offset vers l'adresse de retour = "
             "**40** (32 + 8 octets de saved rbp).")
