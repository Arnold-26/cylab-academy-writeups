# Investigative Reversing 4

**Catégorie** : Forensics · **Challenge** : #54 · **Résolu le** : 2026-11-25

## Énoncé

> investigative-reversing-4-mystery + Item01..05_cp.bmp

## Résolution

Méthode : **LSB après 2019 octets, pas de 12 octets, 10 caractères par image, morceaux en ordre inverse**.

Le binaire `investigative-reversing-4-mystery` lit `Item01.bmp`..`Item05.bmp` et un `flag.txt` de 50 caractères, puis écrit `Item0X_cp.bmp`. La fonction `encodeDataInFile` utilise un en-tete de **2019 octets** (`0x7e3`) et une boucle de 50 caractères (`cmp [rbp-0xc], 0x31`) avec 8 bits (`cmp [rbp-0x10], 7`) et `codedChar` qui écrit dans le **LSB**. La geometrie a été **mesuree** par double exécution : `flag.txt = 'A'*50` puis `'B'*50` (bits 0 et 1 differents), diff des deux sorties pour chacune des 5 images. On obtient 20 octets modifies par image, par paires aux offsets 2019/2020, 2031/2032, 2043/2044... soit un **pas de 12 octets par caractère** et **10 caractères par image**. Reste un piege : l'ordre de lecture des morceaux est **inverse** de celui des images. Les 5 blocs de 10 caractères extraits sont `02e911fb5}` (image 1), `0000000000`, `ng_5k1115_`, `c3_R3ver51`, `academy{N1` (image 5) : il faut les remettre dans l'ordre 5,4,3,2,1 pour obtenir `academy{N1c3_R3ver51ng_5k1115_000000000002e911fb5}`. Sans ce reordonnancement, la chaîne brute contient bien tous les caractères mais ne matche pas le format.

## Flag

```
academy{N1c3_R3ver51ng_5k1115_000000000002e911fb5}
```

## Scripts

- [`solve.py`](../../solve/54/solve.py)
