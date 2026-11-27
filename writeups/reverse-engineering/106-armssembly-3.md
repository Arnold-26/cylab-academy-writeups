# ARMssembly 3

**Catégorie** : Reverse Engineering · **Challenge** : #106 · **Résolu le** : 2026-11-24

## Énoncé

> What integer does this program print?
>
> Flag format: academy{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be academy{0055aabb})
> Use argument a: 605030239
>
> File: [chall_3.S](https://challenge-files.cylabacademy.net/library/e1832c0e785b1f513d13f58ee9c730102098a95b1c2b94e818cb078c96f55475/chall_3.S)

## Résolution

Méthode : **lecture d'assemblee ARM**.

`func1` fait `while (a != 0) { if (a & 1) acc = func2(acc); a >>= 1; }` avec `func2(x)=x+3` : le resultat est `3 * popcount(a)` = 3*12 = 36 = 0x24.

## Flag

```
academy{00000024}
```
