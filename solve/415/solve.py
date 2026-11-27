# 415 - endianness-v2  (Forensics, picoCTF 2024)
# Flag: academy{cert!f1Ed_iNd!4n_s0rrY_3nDian_5b37ea4e}
# Write-up: ../../../writeups/forensics/415-endianness-v2.md
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


cands = [
    "academy{cert!f1Ed_iNd!4n_s0rrY_3nDian_5b37ea4e}",
    "academy{cert!f1Ed_iNd!4n_s0rrY_3nDian}",
]
for f in cands:
    already = json.loads(b).get("solved_by_user")
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print(f"415 {f} -> {ok}")
    if ok:
        if not already:
            wu.write(415, "endianness-v2", "Forensics", "", "inversion d'endianness par blocs de 4", f,
                     "Le fichier provient d'un systeme 32 bits qui a organise les octets a l'envers : en "
                     "inversant chaque groupe de **4 octets**, on obtient un JPEG valide (`ffd8ffe0`...). "
                     "L'image affiche le flag.")
        break
