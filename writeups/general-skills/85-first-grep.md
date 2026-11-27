# First Grep

**Catégorie** : Général Skills · **Difficulté** : Easy · **Épreuve** : picoCTF 2019
**Challenge** : #85

## Énoncé

> Can you find the flag in the file?

**Fichier** : `file (14 546 o)`

## Résolution

`grep -a` du motif de flag dans le fichier (le fichier n'est pas du texte pur, d'où `-a`).

## Flag

```
academy{grep_is_good_to_find_things_b9De1cAb}
```

## Ce qu'il faut retenir

- Toujours `file` + lecture brute avant d'imaginer une technique.
- Le ROT13 et le base64 sont des **encodages**, pas du chiffrement : ils se décodent en une ligne.
- En forensics d'image, l'information utile est souvent dans les **métadonnées**, pas dans les pixels.
