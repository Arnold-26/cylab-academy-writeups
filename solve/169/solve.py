# 169 - It is my Birthday 2  (Cryptography, picoCTF 2021)
# Flag: academy{h4ppy_b1rthd4y_2_m3_8248ffdd}
# Write-up: ../../../writeups/cryptography/169-it-is-my-birthday-2.md
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


f = "academy{h4ppy_b1rthd4y_2_m3_8248ffdd}"
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("169 It is my Birthday 2 ->", ok)
if ok:
    extra = (
        "L'enonce demande d'uploader **deux PDF valides, differents, mais de meme SHA-1**, dont les "
        "**1000 derniers octets** sont identiques a ceux d'un `invite.pdf` fourni. Premier faux diagnostic : "
        "j'ai d'abord tente une collision **MD5** (paire `poeMD5_A/B.pdf` de corkami/collisions, verifiee : "
        "meme MD5 `b347b04f...`, contenus differents) — le service a repondu « You are not invited! ». Le "
        "writeup precise qu'il s'agit de **SHA-1** : le challenge repose sur SHAttered (Stevens et al.), "
        "premiere collision SHA-1 pratique entre deux PDF. Methode : (1) recuperer `shattered-1.pdf` et "
        "`shattered-2.pdf` sur shattered.io (422 435 octets chacun, SHA-1 identique "
        "`38762cf7f55934b3...`, contenus differents — collision a prefixe fixe, donc tout suffixe commun "
        "conserve l'egalite des hashes) ; (2) recuperer l'`invite.pdf` (2 247 830 octets) ; (3) **concatener "
        "a chacun des deux shattered les 1000 derniers octets de l'invite**. Resultat verifie : SHA-1 "
        "`133f99dc4ac356ad...` identique pour les deux fichiers, contenus differents, et les 1000 derniers "
        "octets correspondent bien a l'invite (SHA-1 de la queue : `9bc110fe8b6b5561...`). L'upload renvoie "
        "alors le flag. Points cles : ne pas confondre MD5 et SHA-1 (le nom « Birthday » evoque la collision, "
        "pas l'algorithme) ; et la propriete de collision a prefixe fixe est ce qui permet d'ajouter un "
        "suffixe impose sans casser la collision.")
    print("writeup:", wu.write(169, "It is my Birthday 2", "Cryptography",
                               "invite.pdf + shattered-1/2.pdf (shattered.io)",
                               "collision SHA-1 a prefixe fixe + suffixe impose de 1000 octets",
                               f, extra))
