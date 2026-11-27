# Obedient Cat

**Catégorie** : General Skills · **Difficulté** : Easy · **Épreuve** : picoCTF 2021
**Challenge** : #147

## Énoncé

> This file has a flag in plain sight (aka "in-the-clear").

**Fichier** : `flag (34 o)`

## Résolution

Téléchargement du fichier `flag` puis lecture brute : le flag est le contenu même du fichier.

## Flag

```
academy{s4n1ty_v3r1f13d_61ddac22}
```

## Ce qu'il faut retenir

- Toujours `file` + lecture brute avant d'imaginer une technique.
- Le ROT13 et le base64 sont des **encodages**, pas du chiffrement : ils se décodent en une ligne.
- En forensics d'image, l'information utile est souvent dans les **métadonnées**, pas dans les pixels.
