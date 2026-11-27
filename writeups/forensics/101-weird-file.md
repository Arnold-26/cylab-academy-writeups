# Weird File

**Catégorie** : Forensics · **Challenge** : #101 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **macro VBA en base64**.

Le `.docm` contient un `vbaProject.bin` dont la macro appelle `Shell("python -c 'print(...)'")` avec une chaine **base64** : `YWNhZGVteXttNGNyMHNfcl9kNG5nM3IwdXN9` se decode en flag.

## Flag

```
academy{m4cr0s_r_d4ng3r0us}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_101a.py`](../../solve/101/_z_101a.py)
- [`_z_101b.py`](../../solve/101/_z_101b.py)
- [`_z_101c.py`](../../solve/101/_z_101c.py)
