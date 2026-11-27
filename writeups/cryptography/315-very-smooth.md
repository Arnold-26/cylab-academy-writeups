# Very Smooth

**Catégorie** : Cryptography · **Challenge** : #315 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **Pollard p-1**.

`p-1` est compose de facteurs premiers de **16 bits** alors que `q-1` utilise des facteurs de 17 bits. Un Pollard p-1 avec borne B = 2^16 couvre p-1 mais pas q-1 : `gcd(2^M - 1, n)` donne p.

## Flag

```
academy{p0ll4rd_f4ct0r1z4at10n_FTW_25bd8a39}
```

## Ce qu'il faut retenir

—
