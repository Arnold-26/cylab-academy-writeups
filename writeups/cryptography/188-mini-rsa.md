# Mini RSA

**Catégorie** : Cryptography · **Challenge** : #188 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **exposant petit + balayage de k**.

`e` est petit et `M^e` depasse N de peu : le chiffre vaut `M^e - k*N` pour un petit k. On essaie k=0,1,2,... et on teste si `c + k*N` est une puissance e-ieme parfaite.

## Flag

```
academy{e_sh0u1d_b3_lArg3r_35f26e1a}
```

## Ce qu'il faut retenir

—
