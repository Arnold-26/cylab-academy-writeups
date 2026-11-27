# DISKO 4

**Catégorie** : Forensics · **Challenge** : #704 · **Résolu le** : 2026-11-24

## Énoncé

> Can you find the flag in this disk image?
> This time I deleted the file! Let see you get it now!
> Download the disk image [here](https://challenge-files.cylabacademy.net/library/73410159cc8aafa59ec856dcc13ab8b30a50f6827eef6627d3e346bbd3c0085a/disko-4.dd.gz).

## Résolution

Méthode : **fichier supprime dans FAT32**.

Image FAT32. `fls -r -d` révèle un fichier **supprime** `log/dont-delete.gz` (inode 532021). `icat` le récupère et `gunzip` donne le flag.

## Flag

```
academy{d3l_d0n7_h1d3_w3ll_9748d144}
```

## Scripts

- [`solve.py`](../../solve/704/solve.py)
