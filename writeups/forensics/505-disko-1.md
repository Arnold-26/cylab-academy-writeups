# DISKO 1

**Catégorie** : Forensics · **Challenge** : #505

## Résolution

Image disque gzip : `gunzip` puis `strings` sur le `.dd` — le flag est une chaîne en clair.

## Flag

```
academy{1t5_ju5t_4_5tr1n9_3f5388a2}
```

## Ce qu'il faut retenir

Sur une image disque, `strings` avant tout outil lourd.
