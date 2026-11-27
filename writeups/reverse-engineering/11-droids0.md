# droids0

**Catégorie** : Reverse Engineering · **Challenge** : #11 · **Résolu le** : 2026-11-24

## Énoncé

> Where do droid logs go. Check out this [file](https://challenge-files.cylabacademy.net/library/c763076c81f2aa0246d033d213f4223cbb6ac3cc333b980eb134517010e4024c/zero.apk).

## Résolution

Méthode : **XOR repetitif dans la lib native**.

La lib `libhellojni.so` contient 5 paires (clé, données) et 5 helpers (`marjoram`, `anise`, `oregano`, `sumac`, `pepper`) qui font un **XOR repetitif** `out[i] ^= key[i % keylen]`. Celle-ci : clé `notexist` (0x1a04) sur les données a 0x1a1a. Les autres challenges droids utilisent les autres paires de la même lib.

## Flag

```
academy{a.moose.once.bit.my.sister}
```

## Scripts

- [`solve.py`](../../solve/11/solve.py)
