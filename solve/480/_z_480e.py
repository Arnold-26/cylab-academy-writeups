import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{c1i3nt_s1d3_w3b_s0ck3t5_2327663e}"
st, b = cy.req("GET", "/api/challenges/480/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 480, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"480 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(480, "WebSockFish", "Web Exploitation", "", "WebSocket non authentifie (score d'echecs)", f,
             "Le client envoie au WebSocket `/ws/` un message `eval <score>` (ou `mate <n>`) calcule par "
             "Stockfish. Le serveur **fait confiance au client** : en envoyant `eval -99999`, il croit "
             "perdre lamentablement et donne le flag. Aucune validation cote serveur.")
