# No Padding, No Problem

**Catégorie** : Cryptography · **Challenge** : #154 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **oracle RSA multiplicatif**.

L'oracle refuse le chiffre du flag mais dechiffre tout le reste. On lui donne `c' = c * 2^e mod n` : il rend `m' = 2m mod n`. Comme `2m < n`, on retrouve `m = m' // 2`.

## Flag

```
academy{m4yb3_Th0se_m3s54g3s_4r3_difurrent_86a6d735}
```

## Ce qu'il faut retenir

—
