import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{G07_G07?_d4aea0bd}"
st, b = cy.req("GET", "/api/challenges/449/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 449, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"449 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(449, "format string 3", "Binary Exploitation", "", "GOT overwrite puts -> system", f,
             "Le programme **leak l'adresse de `setvbuf`** puis fait `printf(buf)` (format string) et "
             "`puts(\"/bin/sh\")`. La libc est fournie : `system` = leak - 0x7a3f0 + 0x4f760. Le buffer "
             "est en **position 38** des arguments. On ecrit les 3 moities de `system` (2 octets "
             "chacune, via `%hn`) dans la GOT de `puts` (0x404000) : `puts(\"/bin/sh\")` devient "
             "`system(\"/bin/sh\")` et on obtient un shell.")
