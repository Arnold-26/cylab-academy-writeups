# c0rrupt

**Catégorie** : Forensics · **Challenge** : #53 · **Résolu le** : 2026-11-23

## Énoncé

> We found this [file](https://challenge-files.cylabacademy.net/library/8388ecc430588d15064755583476bec46e23d42a6d8de6e8995c19e40f2e4c58/c0rrupt-mystery). Recover the flag.

## Résolution

Méthode : **reparation manuelle d'un PNG**.

Le fichier à la **signature PNG** et le type `IHDR` corrompus, plus l'en-tete du chunk `IDAT` (longueur et type) detruit. En corrigeant la signature (`89504e47...`), le type `IHDR`, puis en recalculant la longueur et le CRC du chunk `IDAT`, le flux zlib se decompresse et l'image révèle le flag.

## Flag

```
academy{c0rrupt10n_1847995}
```
