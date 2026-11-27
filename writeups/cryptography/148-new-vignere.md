# New Vignere

**Catégorie** : Cryptography · **Challenge** : #148 · **Résolu le** : 2026-11-24

## Énoncé

> Another slight twist on a classic, see if you can recover the flag. (Wrap with academy{})
> [new_vignere.py](https://challenge-files.cylabacademy.net/library/812a0725cb6c07015bb0db4cdd6760bdd47e63cf9b2ad634fe227017f57b7393/new_vignere.py) emfakcakmklfajnnlpekfpkndlmildnmnnljenfckbalpglfnknaonebfcnodkpe

## Résolution

Méthode : **cryptanalyse par contraintes de format**.

Chiffrement = **b16** (chaque octet encode en deux caractères parmi 16) puis **Vigenere** sur un alphabet de 16 lettres. Le flag ne contient que `abcdef0123456789`, donc chaque position paire du clair b16 vaut `d` ou `g` et chaque position impaire `a`-`j`. Ces contraintes determinant la clé (`bickhknij`, longueur 9) sans brute force exhaustif.

## Flag

```
academy{468293b06253c715005873e333d98dbc}
```

## Scripts

- [`solve.py`](../../solve/148/solve.py)
- *4 variantes intermediaires dans `solve/148/archive/`*
