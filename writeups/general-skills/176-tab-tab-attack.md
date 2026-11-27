# Tab, Tab, Attack

**Catégorie** : Général Skills · **Difficulté** : Easy · **Épreuve** : picoCTF 2021
**Challenge** : #176

## Énoncé

> Using tab-complete, navigate through the filesystem to find the flag.

**Fichier** : `Addadshashanammu.zip (4 868 o)`

## Résolution

Décompression du zip, parcours de l'arborescence imbriquée, lecture du binaire final : le flag est en clair dedans.

## Flag

```
academy{l3v3l_up!_t4k3_4_r35t!_9d928112}
```

## Ce qu'il faut retenir

- Toujours `file` + lecture brute avant d'imaginer une technique.
- Le ROT13 et le base64 sont des **encodages**, pas du chiffrement : ils se décodent en une ligne.
- En forensics d'image, l'information utile est souvent dans les **métadonnées**, pas dans les pixels.
