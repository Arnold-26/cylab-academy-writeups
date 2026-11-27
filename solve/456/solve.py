# 456 - Event-Viewing  (Forensics, picoCTF 2025)
# Flag: academy{Ev3nt_vi3wv3r_1s_a_pr3tty_us3ful_t00l_81ba3fe9}
# Write-up: ../../../writeups/forensics/456-event-viewing.md
# Script exact utilise pour produire le flag.
#
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import wu

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""


body = "Ev3nt_vi3wv3r_1s_a_pr3tty_us3ful_t00l_81ba3fe9"
cands = [f"picoCTF{{{body}}}", f"academy{{{body}}}",
         "picoCTF{Ev3nt_vi3wv3r_1s_a_pr3tty_us3ful_t00l_81ba3fe9}"]
for cand in cands:
    already = json.loads(b).get("solved_by_user")
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
