# 705 - Forensics Git 0  (Forensics, picoCTF 2026)
# Flag: academy{g17_1n_7h3_d15k_041217d8}
# Write-up: ../../../writeups/forensics/705-forensics-git-0.md
# This is the script that produced the flag; historical variants are in archive/.
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


f = "academy{g17_1n_7h3_d15k_041217d8}"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"705 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(705, "Forensics Git 0", "Forensics", "", "objets git decompresses (message de commit)", f,
             "Image disque de 1 Go (3 partitions, racine a l'offset 1140736). Un depot git dans "
             "`/home` contient 3 objets : un blob inutile, un tree et un **commit** dont le message dit "
             "« Wrap this phrase in the flag format: g17_1n_7h3_d15k_041217d8 ». Il suffit de "
             "decompresser les objets zlib extraits via `fls`/`icat`.")
