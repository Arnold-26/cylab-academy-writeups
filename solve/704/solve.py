# 704 - DISKO 4  (Forensics, picoCTF 2026)
# Flag: academy{d3l_d0n7_h1d3_w3ll_9748d144}
# Write-up: ../../../writeups/forensics/704-disko-4.md
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


f = "academy{d3l_d0n7_h1d3_w3ll_9748d144}"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"704 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(704, "DISKO 4", "Forensics", "", "fichier supprime dans FAT32", f,
             "Image FAT32. `fls -r -d` revele un fichier **supprime** `log/dont-delete.gz` "
             "(inode 532021). `icat` le recupere et `gunzip` donne le flag.")
