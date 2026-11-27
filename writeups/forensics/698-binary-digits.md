# Binary Digits

**Catégorie** : Forensics · **Challenge** : #698

## Énoncé

> This file doesn't look like much... just a bunch of 1s and 0s. But maybe it's not just random noise. Can you recover anything meaningful from this?
> Download the file [here](https://challenge-files.cylabacademy.net/library/fa557c211c0530127695e5c025ad525fb44b6d41809745cba5f13db15f2a41fe/digits.bin).

## Résolution

`digits.bin` = la représentation binaire d'un JPEG. Regroupement par 8 bits → JPEG reconstruit → l'image affiche le flag.

## Flag

```
academy{h1dd3n_1n_th3_b1n4ry_1b150ee9}
```

## Ce qu'il faut retenir

Un fichier de 0/1 se reconstruit : 8 bits = 1 octet, puis `file` pour reconnaître le format.
