# 721 - Timeline 1  (Forensics, picoCTF 2026)
# Flag: academy{573417h13r_7h4n_7h3_1457_58527bb222}
# Write-up: ../../../writeups/forensics/721-timeline-1.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
import wu

extra = (
    "Image disque ext4 (489 Mo apres gunzip de `timeline-1-partition4.img.gz`). L'enonce demande de "
    "retrouver le flag et de l'envelopper dans `academy{}`. Le writeup donnait l'indice decisif : chercher "
    "un fichier de **49 octets**, cree et **jamais modifie**, en fin de **timeline MAC**. Methode : "
    "`fls -r -m / t721.img` produit un bodyfile au format `MD5|nom|inode|mode|uid|gid|taille|atime|mtime|"
    "ctime|crtime`, ce qui permet de trier par taille ET par date en une passe. Un `awk -F'|' '$7 == 49'` "
    "ne laisse que quatre entrees : deux liens symboliques de certificats (taille 49 par coincidence, mais "
    "type `l/l`) et surtout **`/etc/chat`** (inode 32716), dont les quatre horodatages sont identiques et "
    "valent **1764625807**, la valeur la plus recente de toute l'image (les suivants sont a 1764625325 et "
    "1762891277). C'est exactement le motif « cree, jamais touche, en fin de timeline ». `icat t721.img "
    "32716` extrait 49 octets : `NTczNDE3aDEzcl83aDRuXzdoM18xNDU3XzU4NTI3YmIyMjIK`, du **base64**, qui "
    "se decode en `573417h13r_7h4n_7h3_1457_58527bb222` (leet : « greater than the last… »). Le flag est ce "
    "texte enveloppe dans `academy{}`. Points cles : la commande `-m` (bodyfile) est bien plus efficace que "
    "le listing visuel pour croiser taille et timestamps ; et il faut filtrer sur le **type** en plus de la "
    "taille, puisque des symlinks font aussi 49 octets."
)
ok = wu.write(721, "Timeline 1", "Forensics",
              "timeline-1-partition4.img.gz (image ext4, 489 Mo decompres)",
              "bodyfile fls -m + filtre taille/timestamps -> /etc/chat, base64",
              "academy{573417h13r_7h4n_7h3_1457_58527bb222}", extra)
print("writeup:", ok)
