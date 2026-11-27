# Forensics Git 1

**Catégorie** : Forensics · **Challenge** : #706 · **Résolu le** : 2026-11-24

## Énoncé

> Can you find the flag in this disk image?
> Download the disk image [here](https://challenge-files.cylabacademy.net/library/22372364d5a8dba279cfb716a43ec5352035919f816bcba4bb20fc30297c938c/disk.img.gz).

## Résolution

Méthode : **objet git supprime (historique)**.

Image disque de 1 Go (racine à l'offset 1140736). Le depot git contient 5 objets : un blob avec le flag, un commit « Add flag » qui le référence, puis un commit « Remove flag » qui le supprime de l'arbre. Le blob reste dans `.git/objects` : en decompressant les objets zlib extraits via `fls`/`icat`, on retrouve le flag.

## Flag

```
academy{g17_r3m3mb3r5_d4ddf904}
```

## Scripts

- [`solve.py`](../../solve/706/solve.py)
- *3 variantes intermediaires dans `solve/706/archive/`*
