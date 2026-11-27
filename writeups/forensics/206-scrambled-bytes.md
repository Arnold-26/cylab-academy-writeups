# scrambled-bytes

**Catégorie** : Forensics · **Challenge** : #206 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **seed PRNG + inversion de shuffle**.

`send.py` fait `random.seed(int(time()))`, **shuffle** le fichier, puis envoie chaque octet dans un paquet UDP : port source = `randrange(65536)`, charge = `octet ^ randrange(256)`. Le pcapng contient les paquets (dupliques 2x par la capture). On brute-force le seed autour de l'horodatage du premier paquet en comparant les ports source (6 suffisent), puis on rejoue le PRNG pour annuler le XOR et on **inverse le shuffle** (les swaps se rejouent en ordre inverse, avec `i = N-1-idx`). Le fichier reconstruit est un PNG contenant le flag.

## Flag

```
picoCTF{n0_t1m3_t0_w4st3_5hufflin9_ar0und}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_206a.py`](../../solve/206/_z_206a.py)
- [`_z_206b.py`](../../solve/206/_z_206b.py)
- [`_z_206c.py`](../../solve/206/_z_206c.py)
- [`_z_206d.py`](../../solve/206/_z_206d.py)
- [`_z_206e.py`](../../solve/206/_z_206e.py)
- [`_z_206f.py`](../../solve/206/_z_206f.py)
- [`_z_206g.py`](../../solve/206/_z_206g.py)
- [`_z_206h.py`](../../solve/206/_z_206h.py)
- [`_z_206i.py`](../../solve/206/_z_206i.py)
