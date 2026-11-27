# 11 - droids0  (Reverse Engineering, picoCTF 2019)
# Flag: academy{a.moose.once.bit.my.sister}
# Write-up: ../../../writeups/reverse-engineering/11-droids0.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
for cid, f, name in ((11, "academy{a.moose.once.bit.my.sister}", "droids0"),
                     (14, "academy{a.moose.once.bit.my.sister}", "droids1"),
                     (17, "academy{a.moose.once.bit.my.sister}", "droids4"),
                     (63, "academy{a.moose.once.bit.my.sister}", "droids2")):
    st, b = cy.req("GET", f"/api/challenges/{cid}/")
    already = json.loads(b).get("solved_by_user")
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": cid, "flag": f})
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print(f"{cid} ({name}) deja={already} -> {ok}")
    if ok and not already:
        wu.write(cid, name, "Reverse Engineering", "", "XOR repetitif dans la lib native", f,
                 "La lib `libhellojni.so` contient 5 paires (cle, donnees) et 5 helpers "
                 "(`marjoram`, `anise`, `oregano`, `sumac`, `pepper`) qui font un **XOR repetitif** "
                 "`out[i] ^= key[i % keylen]`. Celle-ci : cle `notexist` (0x1a04) sur les donnees a "
                 "0x1a1a. Les autres challenges droids utilisent les autres paires de la meme lib.")
