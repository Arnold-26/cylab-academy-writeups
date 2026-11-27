# miniRSA

**Catégorie** : Cryptography · **Challenge** : #73 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **petit exposant + balayage de k**.

`e=3` et le message est court (c fait 788 bits contre N=2048) : `c + k*N` est une puissance cubique parfaite. k=0 suffit ici. Racine cubique entiere par bissection.

## Flag

```
academy{n33d_a_lArg3r_e_1106c382}
```

## Ce qu'il faut retenir

—
