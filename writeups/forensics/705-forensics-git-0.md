# Forensics Git 0

**Catégorie** : Forensics · **Challenge** : #705 · **Résolu le** : 2026-11-24

## Énoncé

> Can you find the flag in this disk image?
> Download the disk image [here](https://challenge-files.cylabacademy.net/library/196e14a6a341661d834481bd0dc0c3cd353048d481c003e83b3e62acd05146dc/disk.img.gz).

## Résolution

Méthode : **objets git decompresses (message de commit)**.

Image disque de 1 Go (3 partitions, racine à l'offset 1140736). Un depot git dans `/home` contient 3 objets : un blob inutile, un tree et un **commit** dont le message dit « Wrap this phrase in the flag format: g17_1n_7h3_d15k_041217d8 ». Il suffit de decompresser les objets zlib extraits via `fls`/`icat`.

## Flag

```
academy{g17_1n_7h3_d15k_041217d8}
```

## Scripts

- [`solve.py`](../../solve/705/solve.py)
