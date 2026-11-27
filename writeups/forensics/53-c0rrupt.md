# c0rrupt

**Catégorie** : Forensics · **Challenge** : #53 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **reparation manuelle d'un PNG**.

Le fichier a la **signature PNG** et le type `IHDR` corrompus, plus l'en-tete du chunk `IDAT` (longueur et type) detruit. En corrigeant la signature (`89504e47...`), le type `IHDR`, puis en recalculant la longueur et le CRC du chunk `IDAT`, le flux zlib se decompresse et l'image revele le flag.

## Flag

```
academy{c0rrupt10n_1847995}
```

## Ce qu'il faut retenir

—
