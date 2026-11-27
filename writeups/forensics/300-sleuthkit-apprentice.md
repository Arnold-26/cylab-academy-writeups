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

- [`_z_300_dec.py`](../../solve/300/_z_300_dec.py)
- [`_z_300_pdb.py`](../../solve/300/_z_300_pdb.py)
- [`_z_300_pdb2.py`](../../solve/300/_z_300_pdb2.py)
- [`_z_300_refs.py`](../../solve/300/_z_300_refs.py)
- [`_z_300_va.py`](../../solve/300/_z_300_va.py)
