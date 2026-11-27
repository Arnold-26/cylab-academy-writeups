# WhitePages

**Catégorie** : Forensics · **Challenge** : #51 · **Résolu le** : 2026-11-23

## Énoncé

> I stopped using YellowPages and moved onto WhitePages... but [the page they gave me](https://challenge-files.cylabacademy.net/library/164023ae7e53a7b325e50a82f7cd942427fd0f38084d555c162501500fc475c3/whitepages.txt) is all blank!

## Résolution

Méthode : **stegano par espaces Unicode**.

Le fichier ne contient que deux caractères : l'espace normal (U+0020) et l'espace em (U+2003). En les convertissant en bits (em = 0, espace = 1, MSB d'abord) on reconstitue un texte ASCII qui contient le flag.

## Flag

```
academy{not_all_spaces_are_created_equal_d4c2f3dcae81af992c8e86ddecdf2dd5}
```
