# investigation_encoded_1

**Catégorie** : Forensics · **Challenge** : #47 · **Résolu le** : 2026-11-25

## Énoncé

> mystery (ELF 64 bits non strippe) + image01 (23 octets)

## Résolution

Méthode : **code Huffman maison : matrix (longueur, offset) + pool secret**.

Binaire `mystery` non strippe : `nm`/`readelf` donnent `secret` (0x2020, **37 octets** = 296 bits) et `matrix` (0x2060, **216 octets** = 54 int32 = 27 paires). Le schema est un **code de Huffman code en dur** : pour le symbole k (0..26 = a-z + espace), `matrix[2k]` = longueur du code et `matrix[2k+1]` = offset dans `secret`, le bit i se lisant `(secret[i/8] >> (7 - i%8)) & 1`. Vérification de coherence du mapping par la fréquence : l'indice 4 a le code le plus court (**4 bits**, donc `e`) et l'indice 8 a 6 bits (`i`), ce qui colle à un alphabet a-z + espace. Le fichier `image01` (23 octets, 184 bits) est un **flux de bits** ou les codes traversent les frontieres d'octets, ce qui explique l'échec de tout decodage XOR/base64. En reconstruisant les 27 codes et en matchant glouton le plus court préfixe, on decode `encodedofvzaojsrs` (17 symboles, avec un dernier symbole d'espace qui est du remplissage). **Lecon importante :** le flag est cette chaîne **brute, SANS wrapper `academy{}`** — toutes mes tentatives `academy{...}` et `picoCTF{...}` avaient été refusees, ainsi que les variantes avec espace ou accolade. C'est le même cas que le challenge 36 : quand le decodage produit une chaîne alphanumerique coherente, il faut la soumettre telle quelle avant de supposer un format.

## Flag

```
encodedofvzaojsrs
```

## Scripts

- [`solve.py`](../../solve/47/solve.py)
