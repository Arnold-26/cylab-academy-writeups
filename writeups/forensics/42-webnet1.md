# WebNet1

**Catégorie** : Forensics · **Challenge** : #42 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **TLS RSA decrypte (ssldump) + extraction JPEG**.

TLS 1.2 RSA (`TLS_RSA_WITH_AES_256_GCM_SHA384`). tshark 4.6 a supprime la liste de cles RSA, on utilise donc **ssldump -k** avec la cle convertie en PKCS#1. Le trafic contient une image JPEG (et un leurre `Pico-Flag`) ; le vrai flag est dans un chunk EXIF/commentaire de l'image.

## Flag

```
academy{honey.roasted.peanuts}
```

## Ce qu'il faut retenir

—
