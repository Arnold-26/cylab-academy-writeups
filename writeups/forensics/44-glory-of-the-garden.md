# Glory of the Garden

**Catégorie** : Forensics · **Difficulté** : Easy · **Épreuve** : picoCTF 2019
**Challenge** : #44

## Résolution

`strings -n 8` sur `garden.jpg` : le flag est en clair après les données JPEG.

## Flag

```
academy{more_than_m33ts_the_3y3ff3b9e86}
```

## Ce qu'il faut retenir

Les fichiers image ont souvent des données après l'EOI du JPEG.
