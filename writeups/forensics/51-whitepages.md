# WhitePages

**Catégorie** : Forensics · **Challenge** : #51 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **stegano par espaces Unicode**.

Le fichier ne contient que deux caracteres : l'espace normal (U+0020) et l'espace em (U+2003). En les convertissant en bits (em = 0, espace = 1, MSB d'abord) on reconstitue un texte ASCII qui contient le flag.

## Flag

```
academy{not_all_spaces_are_created_equal_d4c2f3dcae81af992c8e86ddecdf2dd5}
```

## Ce qu'il faut retenir

—
