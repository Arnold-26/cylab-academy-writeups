# interencdec

**Catégorie** : Cryptography · **Challenge** : #418 · **Résolu le** : 2026-11-23

## Énoncé

> Can you get the real meaning from this file.
>
> Download the file [here](https://challenge-files.cylabacademy.net/library/ff83d237e254069296a4d13eb3ff6a79b5a906b779d8ff391f6dd9ceecad43ae/enc_flag).

## Résolution

Méthode : **base64 x2 puis caesar**.

Chaîne en couches : base64 -> base64 -> texte `hjhkltf{jhlzhy_k3jy9wa3k_82243097}` -> Caesar **-7** -> flag. Piege d'ordre : il faut decoder le base64 AVANT de tester le rot13, sinon on déchiffre du bruit.

## Flag

```
academy{caesar_d3cr9pt3d_82243097}
```
