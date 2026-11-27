# Forensics Git 0

**Catégorie** : Forensics · **Challenge** : #705 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **objets git decompresses (message de commit)**.

Image disque de 1 Go (3 partitions, racine a l'offset 1140736). Un depot git dans `/home` contient 3 objets : un blob inutile, un tree et un **commit** dont le message dit « Wrap this phrase in the flag format: g17_1n_7h3_d15k_041217d8 ». Il suffit de decompresser les objets zlib extraits via `fls`/`icat`.

## Flag

```
academy{g17_1n_7h3_d15k_041217d8}
```

## Ce qu'il faut retenir

—

## Scripts

- [`solve.py`](../../solve/705/solve.py)
- *2 variantes intermediaires dans `solve/705/archive/`*
