# Sequences

**Catégorie** : Cryptography · **Challenge** : #129 · **Résolu le** : 2026-11-23

## Énoncé

> Matryoshka dolls are a set of wooden dolls of decreasing size placed one inside another. What's the final one?
> Image: [dolls.jpg](https://challenge-files.cylabacademy.net/library/c48ba7ec3de5a7143687a4363cfa559846283c6f5b87de43d08de59aec195224/dolls.jpg)

## Résolution

Méthode : **images imbriquees (ZIP)**.

Le fichier `dolls.jpg` est en fait un PNG avec un **ZIP ajoute** à l'offset 272492. Chaque ZIP contient l'image suivante, qui contient elle-même un ZIP. Quatre niveaux plus tard, le flag est dans les données de l'image finale.

## Flag

```
academy{ZNTyvSDXRNO1d0xCkBRMhAoiafpCTvgW}
```
