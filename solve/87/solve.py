# 87 - Pitter, Patter, Platters  (Forensics, picoCTF 2020 Mini-Competition)
# Flag: not archived
# Write-up: ../../../writeups/forensics/87-pitter-patter-platters.md
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


f = "academy{b3_5t111_mL|_<3_d18a1e1e}"
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("87 Pitter Patter Platters ->", ok)
if ok:
    wu.write(87, "Pitter, Patter, Platters", "Forensics", "suspicious.dd.sda1 (32 Mo, ext3)",
             "flag dans le slack space, encode UTF-16LE et inverse", f,
             "Image disque ext3 (Tiny Core Linux, 32 Mo). `fls -r -p` montre un fichier "
             "**`suspicious-file.txt`** a la racine (inode 12) qui ne contient que "
             "« Nothing to see here! But you may want to look here --> ». C'est un leurre qui pointe "
             "en fait vers le **slack space** : le fichier fait 55 octets mais occupe un bloc de 1024 "
             "(`istat` donne le bloc direct **2049**). En lisant le bloc entier a l'offset "
             "`2049*1024` et en prenant les octets apres le 55e, on trouve une chaine **UTF-16LE "
             "inversee** (`}` puis `e\\x00` puis `1\\x00` ...). Decodee puis retournee, elle donne "
             "`academy{b3_5t111_mL|_<3_d18a1e1e}`. Pieges : le decodage UTF-16 sur une longueur impaire "
             "produit un caractere de remplacement en tete apres inversion (il faut tronquer a un "
             "nombre pair d'octets), et le fichier leurre ne contient pas le flag — seul le slack le "
             "porte.")
