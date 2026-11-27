# ASCII FTW

**Catégorie** : Reverse Engineering · **Challenge** : #389 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **desassemblage (mov immediats)**.

`objdump -d -M intel` sur main montre une serie de `mov BYTE PTR [rbp-0x..], 0x..` : chaque octet est une lettre du flag en ASCII. On lit la sequence et on decode.

## Flag

```
academy{ASCII_IS_EASY_AC3E0C8C}
```

## Ce qu'il faut retenir

—
