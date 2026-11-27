import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu
cy = CyLab(delay=1.2); cy.login()
f = "academy{fgets_0v3rfl0w42_1ce413d9}"
st, b = cy.req("GET", "/api/challenges/736/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 736, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"736 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(736, "Echo Escape 2", "Binary Exploitation", "", "fgets overflow (offset 44)", f,
             "`char buf[32]` mais `fgets(buf, 128, stdin)` : debordement de 96 octets. Binaire 32 bits "
             "non-PIE, `win()` a 0x080491d6 lit le flag. L'offset vers l'adresse de retour est **44** "
             "(buf[32] + 12 octets de padding du compilateur).")
