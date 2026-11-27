# Enhance!

**Catégorie** : Forensics · **Challenge** : #265 · **Résolu le** : 2026-11-22

## Énoncé

> Download this image file and find the flag.

## Résolution

Méthode : **svg-tspan**.

Le fichier `drawing.flag.svg` est un SVG (XML). Le flag n'est pas dans les metadonnees mais dans le texte vectoriel : chaque caractère est un `<tspan>` sépare. Extraire tous les `<tspan>` et les concaténer dans l'ordre du document donne le flag.

## Flag

```
academy{3nh4nc3d_5b5e6f18}
```
