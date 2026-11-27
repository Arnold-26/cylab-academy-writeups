import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
cands = ["academy{encodedofvzaojsrs}", "academy{encodedeofvzaojsrs}", "academy{encodedofvzaojsrs }"]
for f in cands:
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 47, "flag": f})
    try:
        ok = json.loads(b).get("correct")
    except Exception:
        ok = None
    print("%-34s -> %s" % (f, ok))
    if ok:
        wu.write(47, "investigation_encoded_1", "Forensics", "mystery (ELF) + image01 (23 octets)",
                 "Huffman custom : matrices (bit_len, offset) + pool secret", f,
                 "Le binaire `mystery` n'est pas strippe : `nm`/`readelf` donnent `secret` "
                 "(0x2020, **37 octets** = 296 bits) et `matrix` (0x2060, **216 octets** = 54 int32 = "
                 "27 paires). Le schema est un **code de Huffman code en dur** : pour chaque symbole "
                 "k (0..26 = a-z + espace), `matrix[2k]` = longueur du code et `matrix[2k+1]` = offset "
                 "dans `secret` ; le bit i se lit `(secret[i/8] >> (7 - i%8)) & 1`. L'encodeur "
                 "minuscule l'entree et n'accepte que a-z + espace. Le fichier `image01` (23 octets, "
                 "184 bits) est un **flux de bits** ou les codes traversent les frontieres d'octets "
                 "— d'ou l'echec de tout decodage XOR/base64. En reconstruisant les 27 codes et en "
                 "matchant glouton le plus court prefixe, on decode `encodedofvzaojsrs` ; comme le "
                 "precise le writeup, le message est specifique a l'instance et n'est pas forcement "
                 "au format picoCTF : on l'enveloppe donc dans `academy{...}`.")
        break
