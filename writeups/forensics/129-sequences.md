# Sequences

**Catégorie** : Cryptography · **Challenge** : #129 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **images imbriquees (ZIP)**.

Le fichier `dolls.jpg` est en fait un PNG avec un **ZIP ajoute** a l'offset 272492. Chaque ZIP contient l'image suivante, qui contient elle-meme un ZIP. Quatre niveaux plus tard, le flag est dans les donnees de l'image finale.

## Flag

```
academy{ZNTyvSDXRNO1d0xCkBRMhAoiafpCTvgW}
```
