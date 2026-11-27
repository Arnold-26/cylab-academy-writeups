# File types

**Catégorie** : Forensics · **Challenge** : #268 · **Résolu le** : 2026-11-23

## Énoncé

> This file was found among some files marked confidential but my pdf reader
> cannot read it, maybe yours can.
> You can download the file from [here](https://challenge-files.cylabacademy.net/library/e8f3b5ee39989674877ad03f9ae7fc66f073d82fa2e4a0a8acdaf4b3e62154cb/Flag.pdf).

## Résolution

Méthode : **chaîne de 10 formats imbriques**.

`Flag.pdf` n'est pas un PDF mais une **shell archive** GNU (shar). Chaîne complète : shar -> uuencode -> ar -> cpio -> bzip2 -> gzip -> lzip -> lz4 -> lzma -> lzop -> hexadécimal -> flag. Il faut installer lzip, lz4, zstd et lzop, puis boucler sur `file -b` pour choisir le decompresseur.

## Flag

```
academy{f1len@m3_m@n1pul@t10n_f0r_0b2cur17y_35957b68}
```
