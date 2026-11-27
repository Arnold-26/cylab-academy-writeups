# WebNet1

**Catégorie** : Forensics · **Challenge** : #42 · **Résolu le** : 2026-11-24

## Énoncé

> We found this [packet capture](https://challenge-files.cylabacademy.net/library/afb7599dd63cad30a04eb98d0e4057608120371eb3e8943b632505e32c8b622c/webnet1-capture.pcap) and [key](https://challenge-files.cylabacademy.net/library/afb7599dd63cad30a04eb98d0e4057608120371eb3e8943b632505e32c8b622c/picopico.key). Recover the flag.

## Résolution

Méthode : **TLS RSA decrypte (ssldump) + extraction JPEG**.

TLS 1.2 RSA (`TLS_RSA_WITH_AES_256_GCM_SHA384`). tshark 4.6 a supprime la liste de clés RSA, on utilise donc **ssldump -k** avec la clé convertie en PKCS#1. Le trafic contient une image JPEG (et un leurre `Pico-Flag`) ; le vrai flag est dans un chunk EXIF/commentaire de l'image.

## Flag

```
academy{honey.roasted.peanuts}
```
