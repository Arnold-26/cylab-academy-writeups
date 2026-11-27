# investigation_encoded_2

**Catégorie** : Forensics · **Challenge** : #36 · **Résolu le** : 2026-11-25

## Énoncé

> no_auth_mistery + investigation-encoded-2-output (56 octets)

## Résolution

Méthode : **code Huffman maison : secret 71 o + indexTable (bornes de bits par symbole)**.

Binaire PIE 64 bits avec `secret` (0x1300, 71 octets) et **`indexTable`** (0x1360, 152 octets = 38 int32) - attention, la table ne s'appelle PAS `matrix` ici, ce qui m'avait fait conclure a tort qu'elle etait absente. Contrairement au challenge 47 (paires (len, offset)), `indexTable` contient ici des **bornes de bits** : pour le symbole `ns`, les bits sont `getValue(i)` pour i dans [indexTable[ns], indexTable[ns+1]), avec `getValue(i) = (secret[i/8] >> (7 - i%8)) & 1`. 37 symboles = 26 lettres + 10 chiffres + espace. La normalisation de l'encodeur (lue dans `encode`) est : minuscule, espace -> 0x85, chiffre -> +0x4b, puis `index = (c + 0x12) mod 36` (la division par 36 se reconnait au magic 0x38e38e39 avec un decalage de 3). Il faut donc inverser cette permutation : `c = (ns - 18) mod 36`, avec c<26 -> lettre, sinon chiffre, et ns=36 -> espace. En decodant les 56 octets de sortie (flux de bits MSB-first) par plus-long-prefixe, on obtient `t1m3f1i3500000000000a8bbc8ed` (29 symboles). **Le flag est cette chaine BRUTE, sans wrapper academy{}** - mes tentatives avec `academy{...}` ont toutes ete refusees, alors que la chaine nue est acceptee. Les 10 zeros centraux sont de vrais caracteres, pas du padding.

## Flag

```
t1m3f1i3500000000000a8bbc8ed
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_36a.py`](../../solve/36/_z_36a.py)
- [`_z_36b.sh`](../../solve/36/_z_36b.sh)
- [`_z_36c.sh`](../../solve/36/_z_36c.sh)
- [`_z_36d.sh`](../../solve/36/_z_36d.sh)
- [`_z_36e.sh`](../../solve/36/_z_36e.sh)
- [`_z_36f.py`](../../solve/36/_z_36f.py)
- [`_z_36g.py`](../../solve/36/_z_36g.py)
- [`_z_36h.py`](../../solve/36/_z_36h.py)
- [`_z_36i.py`](../../solve/36/_z_36i.py)
- [`_z_36j.py`](../../solve/36/_z_36j.py)
- [`_z_36k.py`](../../solve/36/_z_36k.py)
