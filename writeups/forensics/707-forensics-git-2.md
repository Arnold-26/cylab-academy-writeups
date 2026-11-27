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

- [`solve.py`](../../solve/707/solve.py)
- *11 variantes intermediaires dans `solve/707/archive/`*
