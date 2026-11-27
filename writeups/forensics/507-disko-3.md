# DISKO 3

**Catégorie** : Forensics · **Challenge** : #507 · **Résolu le** : 2026-11-24

## Énoncé

> Can you find the flag in this disk image?
> This time, its not as plain as you think it is!
> Download the disk image [here](https://challenge-files.cylabacademy.net/library/b1a9c5934b8dd54058ed2cd9d58d057b0e43762f08e5fd32e04a9574fefd5939/disko-3.dd.gz).

## Résolution

Méthode : **FAT32 + flag.gz**.

L'image est un système **FAT32** (pas de table de partitions). Un `fls -r` révèle `/var/log/flag.gz` (inode 522628) ; `icat` l'extrait et `gunzip` donne le flag.

## Flag

```
academy{n3v3r_z1p_2_h1d3_2f899900}
```

## Scripts

- [`solve.py`](../../solve/507/solve.py)
- *1 variantes intermediaires dans `solve/507/archive/`*
