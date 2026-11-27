# Forky

**Catégorie** : Reverse Engineering · **Challenge** : #24 · **Résolu le** : 2026-11-24

## Énoncé

> In [this program](https://challenge-files.cylabacademy.net/library/e8aafd2ba3450ace9c914479a665682e6a98f66ea9eeade3941c4b9a3083f53b/vuln), identify the last integer value that is passed as parameter to the function doNothing().

## Résolution

Méthode : **analyse de fork + mmap partage**.

Le programme `mmap` une zone **partagee** initialisee a 0x3B9ACA00 (1000000000), puis `fork()` 4 fois (16 processus). Chaque processus ajoute 0x499602D2 (1234567890) à la valeur partagee et passe le resultat à `doNothing`. Le dernier appel recoit la valeur après les 16 additions : 1000000000 + 16*1234567890 mod 2^32 = 3573217056.

## Flag

```
academy{-721750240}
```

## Scripts

- [`solve.py`](../../solve/24/solve.py)
