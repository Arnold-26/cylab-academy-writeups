# New Vignere

**Catégorie** : Cryptography · **Challenge** : #148 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **cryptanalyse par contraintes de format**.

Chiffrement = **b16** (chaque octet encode en deux caracteres parmi 16) puis **Vigenere** sur un alphabet de 16 lettres. Le flag ne contient que `abcdef0123456789`, donc chaque position paire du clair b16 vaut `d` ou `g` et chaque position impaire `a`-`j`. Ces contraintes determinant la cle (`bickhknij`, longueur 9) sans brute force exhaustif.

## Flag

```
academy{468293b06253c715005873e333d98dbc}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_148a.py`](../../solve/148/_z_148a.py)
- [`_z_148b.py`](../../solve/148/_z_148b.py)
- [`_z_148c.py`](../../solve/148/_z_148c.py)
- [`_z_148d.py`](../../solve/148/_z_148d.py)
- [`_z_148e.py`](../../solve/148/_z_148e.py)
