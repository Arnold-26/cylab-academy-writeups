# Fresh Java

**Catégorie** : Reverse Engineering · **Challenge** : #271 · **Résolu le** : 2026-11-23

## Énoncé

> Can you get the flag?
> Reverse engineer this [Java program](https://challenge-files.cylabacademy.net/library/8a49236ebd176634e844de1f01d33adf9d0185836ef578fd72b168e513a4eabc/KeygenMe.class).

## Résolution

Méthode : **charAt extraits du bytecode**.

`javap -c -p KeygenMe.class` montre une suite de comparaisons `charAt(N) == bipush <valeur>`. On extrait les paires (indice, code ASCII) et on reconstruit la clé de 34 caractères.

## Flag

```
academy{700l1ng_r3qu1r3d_5e462060}
```
