# ARMssembly 2

**Catégorie** : Reverse Engineering · **Challenge** : #150 · **Résolu le** : 2026-11-24

## Énoncé

> What integer does this program print?
>
> Flag format: academy{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be academy{0055aabb})
> Use argument a: 2729572966
>
> File: [chall_2.S](https://challenge-files.cylabacademy.net/library/fbfcc54038a39e5157f9622cc566610d735af7f60b52cfbe447be69653bd1026/chall_2.S)

## Résolution

Méthode : **lecture d'assemblee ARM**.

`func1` fait `while (i < a) { acc += 3; i++; }` (comparaison **non signee**, `bcc`), donc le resultat est `3*a mod 2^32` = 3*2729572966 = 0xE815EF32.

## Flag

```
academy{e815ef32}
```
