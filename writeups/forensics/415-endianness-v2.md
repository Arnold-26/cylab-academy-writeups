# endianness-v2

**Catégorie** : Forensics · **Challenge** : #415 · **Résolu le** : 2026-11-24

## Énoncé

> Here's a file that was recovered from a 32-bits system that organized the bytes a weird way. We're not even sure what type of file it is.
>
> Download it [here](https://challenge-files.cylabacademy.net/library/ebae1a8eea898c65df654ff8bb94e453e58f8892538546ad9b4aa71e279c2b8d/challengefile) and see what you can get out of it

## Résolution

Méthode : **inversion d'endianness par blocs de 4**.

Le fichier provient d'un système 32 bits qui a organise les octets à l'envers : en inversant chaque groupe de **4 octets**, on obtient un JPEG valide (`ffd8ffe0`...). L'image affiche le flag.

## Flag

```
academy{cert!f1Ed_iNd!4n_s0rrY_3nDian_5b37ea4e}
```

## Scripts

- [`solve.py`](../../solve/415/solve.py)
- *1 variantes intermediaires dans `solve/415/archive/`*
