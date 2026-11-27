# ARMssembly 3

**Catégorie** : Reverse Engineering · **Challenge** : #106 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **lecture d'assemblee ARM**.

`func1` fait `while (a != 0) { if (a & 1) acc = func2(acc); a >>= 1; }` avec `func2(x)=x+3` : le resultat est `3 * popcount(a)` = 3*12 = 36 = 0x24.

## Flag

```
academy{00000024}
```

## Ce qu'il faut retenir

—
