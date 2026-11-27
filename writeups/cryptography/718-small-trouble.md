# Small Trouble

**Catégorie** : Cryptography · **Challenge** : #718 · **Résolu le** : 2026-11-23

## Énoncé

> Everything seems secure; strong numbers, familiar parameters but something small might ruin it all. Can you recover the message?
> Download the [message](https://challenge-files.cylabacademy.net/library/f38c357a8331785ca63ae8e6e36d20e6f8160839a03dc3bdb28e6dcaee33e15f/message.txt). And source [code](https://challenge-files.cylabacademy.net/library/f38c357a8331785ca63ae8e6e36d20e6f8160839a03dc3bdb28e6dcaee33e15f/encryption.py)

## Résolution

Méthode : **d petit -> Wiener**.

`d = getPrime(256)` avec des premiers de 1048 bits : `d < n^0.25`, donc l'**attaque de Wiener** s'applique (fraction continue de e/n, test des convergentes).

## Flag

```
academy{sm4ll_d_c0409804}
```
