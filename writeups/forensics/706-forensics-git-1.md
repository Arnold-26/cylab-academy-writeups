# Forensics Git 1

**Catégorie** : Forensics · **Challenge** : #706 · **Résolu le** : 2026-11-24

## Résolution

Méthode : **objet git supprime (historique)**.

Image disque de 1 Go (racine a l'offset 1140736). Le depot git contient 5 objets : un blob avec le flag, un commit « Add flag » qui le reference, puis un commit « Remove flag » qui le supprime de l'arbre. Le blob reste dans `.git/objects` : en decompressant les objets zlib extraits via `fls`/`icat`, on retrouve le flag.

## Flag

```
academy{g17_r3m3mb3r5_d4ddf904}
```

## Scripts

- [`solve.py`](../../solve/706/solve.py)
- *3 variantes intermediaires dans `solve/706/archive/`*
