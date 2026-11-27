import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
import wu

extra = (
    "Binaire `mystery` non strippe : `nm`/`readelf` donnent `secret` (0x2020, **37 octets** = 296 bits) et "
    "`matrix` (0x2060, **216 octets** = 54 int32 = 27 paires). Le schema est un **code de Huffman code en dur** : "
    "pour le symbole k (0..26 = a-z + espace), `matrix[2k]` = longueur du code et `matrix[2k+1]` = offset dans "
    "`secret`, le bit i se lisant `(secret[i/8] >> (7 - i%8)) & 1`. Verification de coherence du mapping par la "
    "frequence : l'indice 4 a le code le plus court (**4 bits**, donc `e`) et l'indice 8 a 6 bits (`i`), ce qui "
    "colle a un alphabet a-z + espace. Le fichier `image01` (23 octets, 184 bits) est un **flux de bits** ou les "
    "codes traversent les frontieres d'octets, ce qui explique l'echec de tout decodage XOR/base64. En "
    "reconstruisant les 27 codes et en matchant glouton le plus court prefixe, on decode "
    "`encodedofvzaojsrs` (17 symboles, avec un dernier symbole d'espace qui est du remplissage). "
    "**Lecon importante :** le flag est cette chaine **brute, SANS wrapper `academy{}`** — toutes mes tentatives "
    "`academy{...}` et `picoCTF{...}` avaient ete refusees, ainsi que les variantes avec espace ou accolade. "
    "C'est le meme cas que le challenge 36 : quand le decodage produit une chaine alphanumerique coherente, il "
    "faut la soumettre telle quelle avant de supposer un format."
)
ok = wu.write(47, "investigation_encoded_1", "Forensics",
              "mystery (ELF 64 bits non strippe) + image01 (23 octets)",
              "code Huffman maison : matrix (longueur, offset) + pool secret", "encodedofvzaojsrs", extra)
print("writeup 47:", ok)
