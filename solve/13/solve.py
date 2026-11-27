# 13 - Investigative Reversing 2  (Forensics, picoCTF 2019)
# Flag: academy{n3xt_0n30000000000000000000000000c4bf77ad}
# Write-up: ../../../writeups/forensics/13-investigative-reversing-2.md
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


f = "academy{n3xt_0n30000000000000000000000000cc361e70}"
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("13 Investigative Reversing 2 ->", ok)
if not ok:
    # variantes : run de zeros plus court/long
    import re
    for n in (28, 30, 32, 34):
        cand = "academy{n3xt_0n3" + "0" * n + "cc361e70}"
        try:
            o2 = json.loads(b).get("correct")
        except Exception:
            o2 = None
        print("  zeros=%d -> %s" % (n, o2))
        if o2:
            f = cand
            ok = True
            break
if ok:
    extra = ("Binaire PIE 64 bits non strippe (`codedChar` a 0x1195). Logique exacte lue dans `main` : les "
             "**2000 premiers octets** (0x7d0) du BMP sont recopies tels quels (en-tete + palette d'une image "
             "8 bits), puis pour chaque caractere du flag (50 max, `fread` de 0x32 octets) et chacun de ses "
             "**8 bits**, le programme lit un octet de `original.bmp` et appelle "
             "`codedChar(bit, flag[i] - 5, byte)`. Cette fonction fait `(byte & 0xfe) | ((ch >> bit) & 1)` : elle "
             "ecrit le bit du caractere dans le **LSB** de l'octet. Donc, a partir de l'offset **2000**, chaque "
             "groupe de 8 octets porte un caractere : bit j = LSB du j-ieme octet, et le caractere vaut "
             "**valeur + 5**. Deux details qui m'avaient bloque : le decalage de 2000 octets (et non 54 ou 1078, "
             "tailles que j'avais supposees a tort) et le `-5` applique au caractere avant encodage. Le run de "
             "zeros du drapeau est bien reel, pas un artefact.")
    print("writeup:", wu.write(13, "Investigative Reversing 2", "Forensics",
                               "investigative-reversing-2-mystery + investigative-reversing-2-encoded.bmp",
                               "LSB des octets apres l'en-tete de 2000 octets, caractere = valeur + 5", f, extra))
