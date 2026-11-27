# caesar

**Catégorie** : Cryptography · **Challenge** : #64 · **Résolu le** : 2026-11-23

## Énoncé

> Decrypt this message.
> Message: [message](https://challenge-files.cylabacademy.net/library/eb4325fac37933de66857090e6c78c226267394ccaf5c079ff593e3e33b4b95a/data.enc)

## Résolution

Méthode : **caesar : brute force + score**.

Le fichier contient Déjà la forme `academy{...}` — mais l'interieur est le texte chiffre. Il faut decaler l'interieur : 26 essais, score par mots anglais (`the`, `caesar`, ...). Shift 19 donne `crossingtherubicon`.

## Flag

```
academy{crossingtherubiconulqcojpd}
```
