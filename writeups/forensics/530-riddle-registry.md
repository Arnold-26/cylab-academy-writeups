# Riddle Registry

**Catégorie** : Forensics · **Challenge** : #530 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **metadonnees PDF en base64**.

Le PDF contient des metadonnees dont le champ **Author** est en base64 : `YWNhZGVteXtwdXp6bDNkX20zdGFkYXRhX2YwdW5kIV8zY2M3Y2VhOX0=`. Un decodage donne le flag.

## Flag

```
academy{puzzl3d_m3tadata_f0und!_3cc7cea9}
```

## Ce qu'il faut retenir

—

## Scripts

- [`solve.py`](../../solve/530/solve.py)
