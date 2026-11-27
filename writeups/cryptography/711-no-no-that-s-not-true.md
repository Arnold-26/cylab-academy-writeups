# no. no. that's Not TRUe

**Catégorie** : Cryptography · **Challenge** : #711 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **attaque en treillis NTRU (fpylll)**.

NTRU avec des parametres minuscules (N=48, p=3, q=509). On construit le treillis NTRU `[I H ; 0 qI]` (H circulante de h), on le reduit avec **LLL puis BKZ(40)** : les vecteurs courts donnent f (ternaire, norme^2=35). On inverse f mod p par pivot de Gauss pour obtenir f_p_inv, puis `m = f_p_inv * (f*c mod q) mod p` redonne les bits du message.

## Flag

```
academy{th4ts_s0_N0t_TRU3_f5e1dd98}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_711a.py`](../../solve/711/_z_711a.py)
- [`_z_711b.py`](../../solve/711/_z_711b.py)
- [`_z_711c.py`](../../solve/711/_z_711c.py)
- [`_z_711d.py`](../../solve/711/_z_711d.py)
- [`_z_711e.py`](../../solve/711/_z_711e.py)
- [`_z_711f.py`](../../solve/711/_z_711f.py)
- [`_z_711g.py`](../../solve/711/_z_711g.py)
