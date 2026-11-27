# b00tl3gRSA3

**Catégorie** : Cryptography · **Challenge** : #78 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **RSA multiprime + Pollard rho**.

n est un produit de **nombreux petits premiers** (~34 bits). Un Pollard rho recursif les trouve tous ; on reconstruit phi et on dechiffre.

## Flag

```
academy{too_many_fact0rs_4434476}
```
