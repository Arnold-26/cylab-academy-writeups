# interencdec

**Catégorie** : Cryptography · **Challenge** : #418 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **base64 x2 puis caesar**.

Chaine en couches : base64 -> base64 -> texte `hjhkltf{jhlzhy_k3jy9wa3k_82243097}` -> Caesar **-7** -> flag. Piege d'ordre : il faut decoder le base64 AVANT de tester le rot13, sinon on dechiffre du bruit.

## Flag

```
academy{caesar_d3cr9pt3d_82243097}
```

## Ce qu'il faut retenir

—
