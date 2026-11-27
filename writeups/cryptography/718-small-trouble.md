# Small Trouble

**Catégorie** : Cryptography · **Challenge** : #718 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **d petit -> Wiener**.

`d = getPrime(256)` avec des premiers de 1048 bits : `d < n^0.25`, donc l'**attaque de Wiener** s'applique (fraction continue de e/n, test des convergentes).

## Flag

```
academy{sm4ll_d_c0409804}
```
