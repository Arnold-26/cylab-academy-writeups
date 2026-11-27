# Sum-O-Primes

**Catégorie** : Cryptography · **Challenge** : #310 · **Résolu le** : 2026-11-23

## Énoncé

> We have so much faith in RSA we give you not just the product of the primes,
> but their sum as well!
> - [gen.py](https://challenge-files.cylabacademy.net/library/81a018042d8d86e3e85dbdcd77f6b6a1cf6f829182e6fee61f938882ddcf03d2/gen.py)
> - [output.txt](https://challenge-files.cylabacademy.net/library/81a018042d8d86e3e85dbdcd77f6b6a1cf6f829182e6fee61f938882ddcf03d2/output.txt)

## Résolution

Méthode : **n et p+q -> trinome**.

On donne `n = p*q` ET `x = p+q`. p et q sont les racines de `t^2 - x*t + n`, donc `disc = x^2 - 4n`, `p = (x+r)/2`, `q = (x-r)/2` avec `r = isqrt(disc)`.

## Flag

```
academy{pl33z_n0_g1v3_c0ngru3nc3_0f_5qu4r35_2a4c68a9}
```
