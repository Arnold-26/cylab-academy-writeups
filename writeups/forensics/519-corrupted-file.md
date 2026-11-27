# Corrupted file

**Catégorie** : Forensics · **Challenge** : #519

## Énoncé

> This file seems broken... or is it? Maybe a couple of bytes could make all the difference. Can you figure out how to bring it back to life?
> Download the file [here](https://challenge-files.cylabacademy.net/library/217bef66dcb5fd0797e1c0f064b705a73600a8be2e1ebadeab51df5be013109d/file).

## Résolution

Les 2 premiers octets du fichier sont `\x` (littéral) au lieu de `FF D8` (magic JPEG). Remplacement → image lisible.

## Flag

```
academy{r3st0r1ng_th3_by73s_3908f978}
```

## Ce qu'il faut retenir

Un fichier « corrompu » se répare en restaurant sa signature (`FF D8`, `%PDF`, `PK`).
