# Sum-O-Primes

**Catégorie** : Cryptography · **Challenge** : #310 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **n et p+q -> trinome**.

On donne `n = p*q` ET `x = p+q`. p et q sont les racines de `t^2 - x*t + n`, donc `disc = x^2 - 4n`, `p = (x+r)/2`, `q = (x-r)/2` avec `r = isqrt(disc)`.

## Flag

```
academy{pl33z_n0_g1v3_c0ngru3nc3_0f_5qu4r35_2a4c68a9}
```
