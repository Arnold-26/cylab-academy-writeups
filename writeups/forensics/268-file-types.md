# File types

**Catégorie** : Forensics · **Challenge** : #268 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **chaine de 10 formats imbriques**.

`Flag.pdf` n'est pas un PDF mais une **shell archive** GNU (shar). Chaine complete : shar -> uuencode -> ar -> cpio -> bzip2 -> gzip -> lzip -> lz4 -> lzma -> lzop -> hexadecimal -> flag. Il faut installer lzip, lz4, zstd et lzop, puis boucler sur `file -b` pour choisir le decompresseur.

## Flag

```
academy{f1len@m3_m@n1pul@t10n_f0r_0b2cur17y_35957b68}
```
