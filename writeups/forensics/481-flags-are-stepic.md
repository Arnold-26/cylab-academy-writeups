# flags are stepic

**Catégorie** : Forensics · **Challenge** : #481 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **steganographie avec l'outil stepic**.

Le site liste 246 drapeaux de pays. L'un d'eux (`upz.png`) contient un message cache avec l'outil **stepic** (steganographie dans les pixels, pas de simple LSB). `stepic.decode()` revele le flag.

## Flag

```
academy{fl4g_h45_fl4ga947c25f}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_481a.py`](../../solve/481/_z_481a.py)
- [`_z_481b.py`](../../solve/481/_z_481b.py)
- [`_z_481c.py`](../../solve/481/_z_481c.py)
- [`_z_481d.py`](../../solve/481/_z_481d.py)
- [`_z_481e.py`](../../solve/481/_z_481e.py)
- [`_z_481f.py`](../../solve/481/_z_481f.py)
- [`_z_481g.py`](../../solve/481/_z_481g.py)
