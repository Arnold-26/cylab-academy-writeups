# ARMssembly 2

**Catégorie** : Reverse Engineering · **Challenge** : #150 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **lecture d'assemblee ARM**.

`func1` fait `while (i < a) { acc += 3; i++; }` (comparaison **non signee**, `bcc`), donc le resultat est `3*a mod 2^32` = 3*2729572966 = 0xE815EF32.

## Flag

```
academy{e815ef32}
```

## Ce qu'il faut retenir

—
