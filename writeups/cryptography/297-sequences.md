# Sequences

**Catégorie** : Cryptography · **Challenge** : #297 · **Résolu le** : 2026-11-24

## Résolution

Méthode : **exponentiation matricielle**.

La fonction est une **recurrence lineaire d'ordre 4** ; calculer m(2e7) par memoisation explose la pile. On utilise la matrice compagnon 4x4 et l'exponentiation rapide modulo 10^10000 (O(log n) multiplications). Le MD5 du resultat valide la reponse, puis la cle SHA-256 dechiffre le flag.

## Flag

```
academy{b1g_numb3rs_f5b03a75}
```

## Scripts

- [`solve.py`](../../solve/297/solve.py)
- *2 variantes intermediaires dans `solve/297/archive/`*
