# DISKO 2

**Catégorie** : Forensics · **Challenge** : #506 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **partition Linux vs leurres FAT32**.

L'image contient deux partitions : une **Linux** (offset 2048) et une **FAT32** (offset 53248). La FAT32 est remplie de dizaines de faux flags `academy{4_P4Rt_1t_i5_<hash>}`. La bonne partition est la Linux : elle ne contient qu'un seul flag.

## Flag

```
academy{4_P4Rt_1t_i5_fd52d0ab}
```

## Ce qu'il faut retenir

—
