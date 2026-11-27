# not crypto

**Catégorie** : Reverse Engineering · **Challenge** : #222 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **hook LD_PRELOAD sur memcmp**.

Le binaire chiffre l'input (AES) puis compare avec `memcmp` au flag dechiffre present en memoire. Pas besoin de casser l'AES : on intercepte `memcmp` avec un `LD_PRELOAD` qui logue les deux buffers. `n=64` et le premier argument est le flag en clair. `gdb -nx` seul tombait sur les memcmp du loader dynamique (comparaisons de version `GLIBC_2.2.5`), d'ou l'interet du hook qui ne filtre que les comparaisons >= 16 octets.

## Flag

```
picoCTF{c0mp1l3r_0pt1m1z4t10n_15_pur3_w1z4rdry_but_n0_pr0bl3m?}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_222a.sh`](../../solve/222/_z_222a.sh)
- [`_z_222b.sh`](../../solve/222/_z_222b.sh)
- [`_z_222c.sh`](../../solve/222/_z_222c.sh)
- [`_z_222d.sh`](../../solve/222/_z_222d.sh)
- [`_z_222e.sh`](../../solve/222/_z_222e.sh)
- [`_z_222f.sh`](../../solve/222/_z_222f.sh)
- [`_z_222g.py`](../../solve/222/_z_222g.py)
