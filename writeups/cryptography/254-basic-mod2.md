# basic-mod2

**Catégorie** : Cryptography · **Challenge** : #254 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **mod 41 + inverse modulaire**.

Chaque nombre mod 41, puis on prend l'**inverse modulaire** (`pow(r,-1,41)`), puis mapping : 1-26 -> A-Z, 27-36 -> chiffres, 37 -> `_`. L'inverse est l'etape que tout le monde oublie.

## Flag

```
academy{1NV3R53LY_H4RD_950D690F}
```
