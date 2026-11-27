# strings it

**Catégorie** : Général Skills · **Difficulté** : Easy · **Épreuve** : picoCTF 2019

## Énoncé

> Can you find the flag in [file](https://challenge-files.cylabacademy.net/library/badce1db694f2fe71ecd915ef2eeb78d799c90b1bc230960ce03ef0074573616/strings) without running it?

**Challenge** : #37

## Résolution

`strings -n 6` sur le binaire puis grep du motif de flag.

## Flag

```
academy{5tRIng5_1T_0c2e1fc3}
```

## Ce qu'il faut retenir

`strings` révèle le texte lisible sans exécuter le binaire.
