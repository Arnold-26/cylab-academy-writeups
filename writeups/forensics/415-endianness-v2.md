# endianness-v2

**Catégorie** : Forensics · **Challenge** : #415 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **inversion d'endianness par blocs de 4**.

Le fichier provient d'un systeme 32 bits qui a organise les octets a l'envers : en inversant chaque groupe de **4 octets**, on obtient un JPEG valide (`ffd8ffe0`...). L'image affiche le flag.

## Flag

```
academy{cert!f1Ed_iNd!4n_s0rrY_3nDian_5b37ea4e}
```

## Ce qu'il faut retenir

—

## Scripts

- [`solve.py`](../../solve/415/solve.py)
- *1 variantes intermediaires dans `solve/415/archive/`*
