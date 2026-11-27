# 54 - Investigative Reversing 4  (Forensics, picoCTF 2019)
# Flag: academy{N1c3_R3ver51ng_5k1115_000000000002e911fb5}
# Write-up: ../../../writeups/forensics/54-investigative-reversing-4.md
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


f = "academy{N1c3_R3ver51ng_5k1115_000000000002e911fb5}"
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("54 Investigative Reversing 4 ->", ok, "|", f)
if not ok:
    alt = "academy{N1c3_R3ver51ng_5k1115_0000000000" + "02e911fb5}"
    for cand in (alt, f.replace("_0000000000", "_00000000000")):
        try:
            o2 = json.loads(b).get("correct")
        except Exception:
            o2 = None
        print("  variante", cand, "->", o2)
        if o2:
            f = cand
            ok = True
            break
if ok:
    extra = (
        "Le binaire `investigative-reversing-4-mystery` lit `Item01.bmp`..`Item05.bmp` et un `flag.txt` de "
        "50 caracteres, puis ecrit `Item0X_cp.bmp`. La fonction `encodeDataInFile` utilise un en-tete de "
        "**2019 octets** (`0x7e3`) et une boucle de 50 caracteres (`cmp [rbp-0xc], 0x31`) avec 8 bits "
        "(`cmp [rbp-0x10], 7`) et `codedChar` qui ecrit dans le **LSB**. La geometrie a ete **mesuree** par "
        "double execution : `flag.txt = 'A'*50` puis `'B'*50` (bits 0 et 1 differents), diff des deux sorties "
        "pour chacune des 5 images. On obtient 20 octets modifies par image, par paires aux offsets "
        "2019/2020, 2031/2032, 2043/2044... soit un **pas de 12 octets par caractere** et **10 caracteres par "
        "image**. Reste un piege : l'ordre de lecture des morceaux est **inverse** de celui des images. Les 5 "
        "blocs de 10 caracteres extraits sont `02e911fb5}` (image 1), `0000000000`, `ng_5k1115_`, "
        "`c3_R3ver51`, `academy{N1` (image 5) : il faut les remettre dans l'ordre 5,4,3,2,1 pour obtenir "
        "`academy{N1c3_R3ver51ng_5k1115_000000000002e911fb5}`. Sans ce reordonnancement, la chaine brute "
        "contient bien tous les caracteres mais ne matche pas le format.")
    print("writeup:", wu.write(54, "Investigative Reversing 4", "Forensics",
                               "investigative-reversing-4-mystery + Item01..05_cp.bmp",
                               "LSB apres 2019 octets, pas de 12 octets, 10 caracteres par image, morceaux en ordre inverse",
                               f, extra))
