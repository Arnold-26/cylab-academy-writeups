# DISKO 2

**Catégorie** : Forensics · **Challenge** : #506 · **Résolu le** : 2026-11-23

## Énoncé

> Can you find the flag in this disk image?
> The right one is Linux! One wrong step and its all gone!
> Download the disk image [here](https://challenge-files.cylabacademy.net/library/8ab9d410ce0403ed59f601f295f649ead92bfbf5deeb729832d2574db8d52d94/disko-2.dd.gz).

## Résolution

Méthode : **partition Linux vs leurres FAT32**.

L'image contient deux partitions : une **Linux** (offset 2048) et une **FAT32** (offset 53248). La FAT32 est remplie de dizaines de faux flags `academy{4_P4Rt_1t_i5_<hash>}`. La bonne partition est la Linux : elle ne contient qu'un seul flag.

## Flag

```
academy{4_P4Rt_1t_i5_fd52d0ab}
```
