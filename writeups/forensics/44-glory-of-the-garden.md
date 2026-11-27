# Glory of the Garden

**Catégorie** : Forensics · **Difficulté** : Easy · **Épreuve** : picoCTF 2019

## Énoncé

> This file contains more than it seems.
> Get the flag from [garden.jpg](https://challenge-files.cylabacademy.net/library/3c60c5a7f7a8067606c51d4b4b3c7913fae709b11e2f2c7adbc0a0b4cda452ff/garden.jpg).

**Challenge** : #44

## Résolution

`strings -n 8` sur `garden.jpg` : le flag est en clair après les données JPEG.

## Flag

```
academy{more_than_m33ts_the_3y3ff3b9e86}
```

## Ce qu'il faut retenir

Les fichiers image ont souvent des données après l'EOI du JPEG.
