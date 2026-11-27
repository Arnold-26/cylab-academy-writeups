import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=1.2)
cy.login()
cands = [
    "academy{N0t_a_StaT31355g}",
    "academy{N0t_a_StaT31355e}",
    "academy{N0t_a_StaT31355_g}",
    "academy{N0t_a_StaT31355e_g}",
    "academy{N0t_a_StaT31355}",
    "academy{N0t_a_StaT31355g}_36f6e6",
    "academy{N0t_a_StaT31355e}_36f6e6",
]
for f in cands:
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 84, "flag": f})
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print(f"84 {f} -> {ok}")
    if ok:
        break
