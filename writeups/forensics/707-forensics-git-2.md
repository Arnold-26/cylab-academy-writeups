# Forensics Git 2

**Catégorie** : Forensics · **Challenge** : #707 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **objets git decompresses**.

Image disque de 1 Go (3 partitions ; la racine est a l'offset 1140736). Un depot git se trouve dans `/home/ctf-player/Code/killer-chat-app/.git`. J'ai extrait les objets via `fls`/`icat` puis decompresse chaque objet zlib : le flag est dans l'un des blobs.

## Flag

```
academy{g17_r35cu3_16ac6bf3}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_707a.sh`](../../solve/707/_z_707a.sh)
- [`_z_707b.sh`](../../solve/707/_z_707b.sh)
- [`_z_707c.sh`](../../solve/707/_z_707c.sh)
- [`_z_707d.sh`](../../solve/707/_z_707d.sh)
- [`_z_707e.sh`](../../solve/707/_z_707e.sh)
- [`_z_707f.sh`](../../solve/707/_z_707f.sh)
- [`_z_707g.sh`](../../solve/707/_z_707g.sh)
- [`_z_707h.sh`](../../solve/707/_z_707h.sh)
- [`_z_707i.sh`](../../solve/707/_z_707i.sh)
- [`_z_707j.sh`](../../solve/707/_z_707j.sh)
- [`_z_707k.py`](../../solve/707/_z_707k.py)
- [`_z_707l.py`](../../solve/707/_z_707l.py)
