import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
import wu

extra = (
    "Binaire PIE 64 bits avec `secret` (0x1300, 71 octets) et **`indexTable`** (0x1360, 152 octets = 38 int32) "
    "- attention, la table ne s'appelle PAS `matrix` ici, ce qui m'avait fait conclure a tort qu'elle etait absente. "
    "Contrairement au challenge 47 (paires (len, offset)), `indexTable` contient ici des **bornes de bits** : pour le "
    "symbole `ns`, les bits sont `getValue(i)` pour i dans [indexTable[ns], indexTable[ns+1]), avec "
    "`getValue(i) = (secret[i/8] >> (7 - i%8)) & 1`. 37 symboles = 26 lettres + 10 chiffres + espace. "
    "La normalisation de l'encodeur (lue dans `encode`) est : minuscule, espace -> 0x85, chiffre -> +0x4b, puis "
    "`index = (c + 0x12) mod 36` (la division par 36 se reconnait au magic 0x38e38e39 avec un decalage de 3). Il faut "
    "donc inverser cette permutation : `c = (ns - 18) mod 36`, avec c<26 -> lettre, sinon chiffre, et ns=36 -> espace. "
    "En decodant les 56 octets de sortie (flux de bits MSB-first) par plus-long-prefixe, on obtient "
    "`t1m3f1i3500000000000a8bbc8ed` (29 symboles). **Le flag est cette chaine BRUTE, sans wrapper academy{}** - mes "
    "tentatives avec `academy{...}` ont toutes ete refusees, alors que la chaine nue est acceptee. Les 10 zeros "
    "centraux sont de vrais caracteres, pas du padding."
)
ok = wu.write(36, "investigation_encoded_2", "Forensics",
              "no_auth_mistery + investigation-encoded-2-output (56 octets)",
              "code Huffman maison : secret 71 o + indexTable (bornes de bits par symbole)",
              "t1m3f1i3500000000000a8bbc8ed", extra)
print("writeup 36:", ok)
