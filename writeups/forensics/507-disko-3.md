# DISKO 3

**Catégorie** : Forensics · **Challenge** : #507 · **Résolu le** : 2026-11-24

## Résolution

Méthode : **FAT32 + flag.gz**.

L'image est un systeme **FAT32** (pas de table de partitions). Un `fls -r` revele `/var/log/flag.gz` (inode 522628) ; `icat` l'extrait et `gunzip` donne le flag.

## Flag

```
academy{n3v3r_z1p_2_h1d3_2f899900}
```

## Scripts

- [`solve.py`](../../solve/507/solve.py)
- *1 variantes intermediaires dans `solve/507/archive/`*
