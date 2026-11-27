# 530 - Riddle Registry  (Forensics, picoMini by CMU-Africa)
# Flag: academy{puzzl3d_m3tadata_f0und!_3cc7cea9}
# Write-up: ../../../writeups/forensics/530-riddle-registry.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
st, b = cy.req("GET", "/api/challenges/530/")
print("530 deja resolu:", json.loads(b).get("solved_by_user"))
f = "academy{puzzl3d_m3tadata_f0und!_3cc7cea9}"
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 530, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print("530 ->", ok)
if ok:
    wu.write(530, "Riddle Registry", "Forensics", "", "metadonnees PDF en base64", f,
             "Le PDF contient des metadonnees dont le champ **Author** est en base64 : "
             "`YWNhZGVteXtwdXp6bDNkX20zdGFkYXRhX2YwdW5kIV8zY2M3Y2VhOX0=`. Un decodage donne le flag.")
