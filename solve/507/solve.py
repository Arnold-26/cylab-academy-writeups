# 507 - DISKO 3  (Forensics, ?)
# Flag: academy{n3v3r_z1p_2_h1d3_2f899900}
# Write-up: ../../../writeups/forensics/507-disko-3.md
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


f = "academy{n3v3r_z1p_2_h1d3_2f899900}"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"507 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(507, "DISKO 3", "Forensics", "", "FAT32 + flag.gz", f,
             "L'image est un systeme **FAT32** (pas de table de partitions). Un `fls -r` revele "
             "`/var/log/flag.gz` (inode 522628) ; `icat` l'extrait et `gunzip` donne le flag.")
