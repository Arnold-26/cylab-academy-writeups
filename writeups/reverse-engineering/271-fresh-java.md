# Fresh Java

**Catégorie** : Reverse Engineering · **Challenge** : #271 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **charAt extraits du bytecode**.

`javap -c -p KeygenMe.class` montre une suite de comparaisons `charAt(N) == bipush <valeur>`. On extrait les paires (indice, code ASCII) et on reconstruit la cle de 34 caracteres.

## Flag

```
academy{700l1ng_r3qu1r3d_5e462060}
```

## Ce qu'il faut retenir

—
