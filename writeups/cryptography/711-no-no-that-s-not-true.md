# no. no. that's Not TRUe

**Catégorie** : Cryptography · **Challenge** : #711 · **Résolu le** : 2026-11-24

## Énoncé

> no. no. that's Not TRUe. that's impossible!
>
> Download [encryption script](https://challenge-files.cylabacademy.net/library/bf8aba3877c02751332b4ac7689f2ee42a142af38a7753e8173ccddc403e4360/encrypt.py) and [public info](https://challenge-files.cylabacademy.net/library/bf8aba3877c02751332b4ac7689f2ee42a142af38a7753e8173ccddc403e4360/public.txt).

## Résolution

Méthode : **attaque en treillis NTRU (fpylll)**.

NTRU avec des parametres minuscules (N=48, p=3, q=509). On construit le treillis NTRU `[I H ; 0 qI]` (H circulante de h), on le reduit avec **LLL puis BKZ(40)** : les vecteurs courts donnent f (ternaire, norme^2=35). On inverse f mod p par pivot de Gauss pour obtenir f_p_inv, puis `m = f_p_inv * (f*c mod q) mod p` redonne les bits du message.

## Flag

```
academy{th4ts_s0_N0t_TRU3_f5e1dd98}
```

## Scripts

- [`solve.py`](../../solve/711/solve.py)
