import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "088d0d0dfed3a7c041027e01d85e0887"
st, b = cy.req("GET", "/api/challenges/167/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 167, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"167 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(167, "Binary Gauntlet 0", "Binary Exploitation", "", "buffer overflow -> SIGSEGV handler", f,
             "Le programme lit le flag dans un buffer global, installe un **handler SIGSEGV** qui "
             "l'imprime, puis fait `strcpy(dest[128], input)` sans verifier la taille. Il suffit "
             "d'envoyer 144 octets + une adresse invalide pour ecraser l'adresse de retour, provoquer "
             "un segfault et faire afficher le flag.")
