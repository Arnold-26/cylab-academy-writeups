# StegoRSA

**Catégorie** : Cryptography · **Challenge** : #719 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **cle privee cachee dans l'EXIF**.

`image.jpg` porte la cle privee RSA dans son champ EXIF **Comment**, encodee en hexadecimal. On decode le hex, on ecrit le PEM, puis `openssl pkeyutl -decrypt -inkey priv.pem -in flag.enc`.

## Flag

```
academy{rs4_k3y_1n_1mg_d97b7bfb}
```

## Ce qu'il faut retenir

—
