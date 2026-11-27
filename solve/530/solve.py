# 530 - Riddle Registry  (Forensics, picoMini by CMU-Africa)
# Flag: academy{puzzl3d_m3tadata_f0und!_3cc7cea9}
# Write-up: ../../../writeups/forensics/530-riddle-registry.md
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


print("530 deja resolu:", json.loads(b).get("solved_by_user"))
f = "academy{puzzl3d_m3tadata_f0und!_3cc7cea9}"
ok = json.loads(b).get("correct") if b.startswith("{") else None
print("530 ->", ok)
if ok:
    wu.write(530, "Riddle Registry", "Forensics", "", "metadonnees PDF en base64", f,
             "Le PDF contient des metadonnees dont le champ **Author** est en base64 : "
             "`YWNhZGVteXtwdXp6bDNkX20zdGFkYXRhX2YwdW5kIV8zY2M3Y2VhOX0=`. Un decodage donne le flag.")
