# b00tl3gRSA3

**Catégorie** : Cryptography · **Challenge** : #78 · **Résolu le** : 2026-11-23

## Énoncé

> Why use p and q when I can use more?

## Résolution

Méthode : **RSA multiprime + Pollard rho**.

n est un produit de **nombreux petits premiers** (~34 bits). Un Pollard rho recursif les trouve tous ; on reconstruit phi et on déchiffre.

## Flag

```
academy{too_many_fact0rs_4434476}
```
