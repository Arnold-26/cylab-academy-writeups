# ClusterRSA

**Catégorie** : Cryptography · **Challenge** : #702 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **RSA multiprime (4 facteurs)**.

Le module `n` a **4 facteurs premiers** (RSA multiprime). factordb les donne, on calcule `phi = produit(p_i - 1)` puis `d = e^-1 mod phi` et on dechiffre.

## Flag

```
academy{mul71_rsa_411fc267}
```
