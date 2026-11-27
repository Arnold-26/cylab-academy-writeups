# Sleuthkit Apprentice

**Catégorie** : Forensics · **Challenge** : #300 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **icat sur inode UTF-16**.

L'image contient deux partitions Linux. Dans la seconde (offset 360448), `fls -r` revele `my_folder/flag.uni.txt`. Le fichier est encode en **UTF-16 LE**, d'ou les octets nuls entre les caracteres ; `icat` le restitue directement.

## Flag

```
academy{by73_5urf3r_6395be48}
```

## Ce qu'il faut retenir

—

## Scripts

- [`solve.py`](../../solve/300/solve.py)
- *4 variantes intermediaires dans `solve/300/archive/`*
