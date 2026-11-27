import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{L34k1ng_Fl4g_0ff_St4ck_9f22d2dd}"
st, b = cy.req("GET", "/api/challenges/269/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 269, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"269 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(269, "flag leak", "Binary Exploitation", "", "format string leak (%20$s)", f,
             "`printf(story)` sur une entree `scanf(\"%127s\")`. Le flag est lu dans un buffer LOCAL de "
             "`vuln`, donc present sur la pile. En scannant `%<n>$s` pour n de 1 a 30, la position "
             "**20** pointe directement sur le buffer du flag et l'affiche.")
