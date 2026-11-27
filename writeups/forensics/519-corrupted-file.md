# Corrupted file

**Catégorie** : Forensics · **Challenge** : #519

## Résolution

Les 2 premiers octets du fichier sont `\x` (littéral) au lieu de `FF D8` (magic JPEG). Remplacement → image lisible.

## Flag

```
academy{r3st0r1ng_th3_by73s_3908f978}
```

## Ce qu'il faut retenir

Un fichier « corrompu » se répare en restaurant sa signature (`FF D8`, `%PDF`, `PK`).
