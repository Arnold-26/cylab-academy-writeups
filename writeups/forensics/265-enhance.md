# Enhance!

**Catégorie** : Forensics · **Challenge** : #265 · **Résolu le** : 2026-11-22

## Énoncé

> Download this image file and find the flag.

## Résolution

Méthode : **svg-tspan**.

Le fichier `drawing.flag.svg` est un SVG (XML). Le flag n'est pas dans les metadonnees mais dans le texte vectoriel : chaque caractere est un `<tspan>` separe. Extraire tous les `<tspan>` et les concatener dans l'ordre du document donne le flag.

## Flag

```
academy{3nh4nc3d_5b5e6f18}
```

## Ce qu'il faut retenir

—
