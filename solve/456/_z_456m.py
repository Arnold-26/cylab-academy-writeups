import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
body = "Ev3nt_vi3wv3r_1s_a_pr3tty_us3ful_t00l_81ba3fe9"
cands = [f"picoCTF{{{body}}}", f"academy{{{body}}}",
         "picoCTF{Ev3nt_vi3wv3r_1s_a_pr3tty_us3ful_t00l_81ba3fe9}"]
for cand in cands:
    st, b = cy.req("GET", "/api/challenges/456/")
    already = json.loads(b).get("solved_by_user")
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 456, "flag": cand})
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print(f"456 {cand} -> {ok}")
    if ok:
        if not already:
            wu.write(456, "Event-Viewing", "Forensics", "", "evtx : fragments base64 dans 3 evenements", cand,
                     "Le log contient l'installation de `Totally_Legit_Software.msi` (1033/1040), une "
                     "modification de registre (4657) pointant vers `custom_shutdown.exe`, et un "
                     "arret force (1074) dont le champ `param6` contient la fin du flag en base64 "
                     "(`dDAwbF84MWJhM2ZlOX0=` -> `t00l_81ba3fe9}`).")
        break
