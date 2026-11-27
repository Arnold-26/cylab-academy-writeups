# Wave a flag

**Catégorie** : General Skills · **Difficulté** : Easy · **Épreuve** : picoCTF 2021
**Challenge** : #170

## Énoncé

> Can you invoke help flags for a tool or binary? This program has extraordinarily helpful information...

**Fichier** : `warm (17 368 o, ELF)`

## Résolution

Binaire ELF téléchargé, `chmod +x`, puis recherche du flag dans la sortie (`--help`). Le flag est imprimé par le programme.

## Flag

```
academy{b1scu1ts_4nd_gr4vy_57d8c79}
```

## Ce qu'il faut retenir

- Toujours `file` + lecture brute avant d'imaginer une technique.
- Le ROT13 et le base64 sont des **encodages**, pas du chiffrement : ils se décodent en une ligne.
- En forensics d'image, l'information utile est souvent dans les **métadonnées**, pas dans les pixels.
