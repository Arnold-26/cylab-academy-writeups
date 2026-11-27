# information

**Catégorie** : Forensics · **Difficulté** : Easy · **Épreuve** : picoCTF 2021
**Challenge** : #186

## Énoncé

> Files can always be changed in a secret way. Can you find the secret?

**Fichier** : `cat.jpg (878 136 o)`

## Résolution

`exiftool` sur l'image. Le champ **License** contient une chaîne base64 `YWNhZGVteXt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9` → décodée, elle donne le flag. Le champ Copyright (« PicoCTF ») ne sert que d'indice.

## Flag

```
academy{the_m3tadata_1s_modified}
```

## Ce qu'il faut retenir

- Toujours `file` + lecture brute avant d'imaginer une technique.
- Le ROT13 et le base64 sont des **encodages**, pas du chiffrement : ils se décodent en une ligne.
- En forensics d'image, l'information utile est souvent dans les **métadonnées**, pas dans les pixels.
