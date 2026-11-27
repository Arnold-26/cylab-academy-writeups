# DISKO 4

**Catégorie** : Forensics · **Challenge** : #704 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **fichier supprime dans FAT32**.

Image FAT32. `fls -r -d` revele un fichier **supprime** `log/dont-delete.gz` (inode 532021). `icat` le recupere et `gunzip` donne le flag.

## Flag

```
academy{d3l_d0n7_h1d3_w3ll_9748d144}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_704a.sh`](../../solve/704/_z_704a.sh)
- [`_z_704b.sh`](../../solve/704/_z_704b.sh)
- [`_z_704c.sh`](../../solve/704/_z_704c.sh)
- [`_z_704d.py`](../../solve/704/_z_704d.py)
