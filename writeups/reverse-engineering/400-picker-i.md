# Picker I

**Catégorie** : Reverse Engineering · **Challenge** : #400 · **Résolu le** : 2026-11-23

## Énoncé

> This service can provide you with a random number, but can it do anything else?

## Résolution

Méthode : **eval(user_input+'()')**.

Le programme fait `eval(user_input + '()')`. Il suffit de taper `win` pour appeler la fonction qui affiche le flag (en hex, a decoder).

## Flag

```
academy{4_d14m0nd_1n_7h3_r0ugh_193d362d}
```
