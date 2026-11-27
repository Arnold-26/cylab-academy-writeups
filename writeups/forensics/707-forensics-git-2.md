# Forensics Git 2

**Catégorie** : Forensics · **Challenge** : #707 · **Résolu le** : 2026-11-24

## Énoncé

> The agents interrupted the perpetrator's disk deletion routine. Can you recover
> this git repo?
> Download the disk image [here](https://challenge-files.cylabacademy.net/library/3a43e336226c70fa1460010185a75eb66bc11c41594c75e9eb5122f1b91b7b22/disk.img.gz).

## Résolution

Méthode : **objets git decompresses**.

Image disque de 1 Go (3 partitions ; la racine est à l'offset 1140736). Un depot git se trouve dans `/home/ctf-player/Code/killer-chat-app/.git`. J'ai extrait les objets via `fls`/`icat` puis decompresse chaque objet zlib : le flag est dans l'un des blobs.

## Flag

```
academy{g17_r35cu3_16ac6bf3}
```

## Scripts

- [`solve.py`](../../solve/707/solve.py)
