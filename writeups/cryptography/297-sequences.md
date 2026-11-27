# Sequences

**Catégorie** : Cryptography · **Challenge** : #297 · **Résolu le** : 2026-11-24

## Énoncé

> I wrote this linear recurrence function, can you figure out how to make it run
> fast enough and get the flag?
> Download the code here [sequences.py](https://challenge-files.cylabacademy.net/library/45d82e383fd50225799f78790618dca400da46d59748762e022b12e4aafaebd3/sequences.py)
>
> Note that even an efficient solution might take several seconds to run. If your
> solution is taking several minutes, then you may need to reconsider your
> approach.

## Résolution

Méthode : **exponentiation matricielle**.

La fonction est une **recurrence lineaire d'ordre 4** ; calculer m(2e7) par memoisation explose la pile. On utilise la matrice compagnon 4x4 et l'exponentiation rapide modulo 10^10000 (O(log n) multiplications). Le MD5 du resultat valide la réponse, puis la clé SHA-256 déchiffre le flag.

## Flag

```
academy{b1g_numb3rs_f5b03a75}
```

## Scripts

- [`solve.py`](../../solve/297/solve.py)
