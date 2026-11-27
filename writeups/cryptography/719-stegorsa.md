# StegoRSA

**Catégorie** : Cryptography · **Challenge** : #719 · **Résolu le** : 2026-11-23

## Énoncé

> A message has been encrypted using RSA. The public key is gone… but someone might have been careless with the private key. Can you recover it and decrypt the message?
> Download the [flag](https://challenge-files.cylabacademy.net/library/4c19613e66e3f22baabf929555a826f8ebd997a002b008eb4e51dc2849aca14e/flag.enc) and [image](https://challenge-files.cylabacademy.net/library/4c19613e66e3f22baabf929555a826f8ebd997a002b008eb4e51dc2849aca14e/image.jpg).

## Résolution

Méthode : **clé privee cachee dans l'EXIF**.

`image.jpg` porte la clé privee RSA dans son champ EXIF **Comment**, encodee en hexadécimal. On decode le hex, on écrit le PEM, puis `openssl pkeyutl -decrypt -inkey priv.pem -in flag.enc`.

## Flag

```
academy{rs4_k3y_1n_1mg_d97b7bfb}
```
