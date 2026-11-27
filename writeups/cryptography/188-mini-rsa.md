# Mini RSA

**Catégorie** : Cryptography · **Challenge** : #188 · **Résolu le** : 2026-11-23

## Énoncé

> What happens if you have a small exponent? There is a twist though, we padded the plaintext so that $$(M ** e)$$ is just barely larger than $$N$$. Let's decrypt this:
> [values](https://challenge-files.cylabacademy.net/library/28a2479cff9eab20837067152fcead0a079e378b38249280192aef28a975269a/values)

## Résolution

Méthode : **exposant petit + balayage de k**.

`e` est petit et `M^e` depasse N de peu : le chiffre vaut `M^e - k*N` pour un petit k. On essaie k=0,1,2,... et on teste si `c + k*N` est une puissance e-ieme parfaite.

## Flag

```
academy{e_sh0u1d_b3_lArg3r_35f26e1a}
```
