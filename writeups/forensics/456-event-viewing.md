# Event-Viewing

**Catégorie** : Forensics · **Challenge** : #456 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **evtx : fragments base64 dans 3 evenements**.

Le log contient l'installation de `Totally_Legit_Software.msi` (1033/1040), une modification de registre (4657) pointant vers `custom_shutdown.exe`, et un arret force (1074) dont le champ `param6` contient la fin du flag en base64 (`dDAwbF84MWJhM2ZlOX0=` -> `t00l_81ba3fe9}`).

## Flag

```
academy{Ev3nt_vi3wv3r_1s_a_pr3tty_us3ful_t00l_81ba3fe9}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_456a.sh`](../../solve/456/_z_456a.sh)
- [`_z_456b.py`](../../solve/456/_z_456b.py)
- [`_z_456c.py`](../../solve/456/_z_456c.py)
- [`_z_456d.py`](../../solve/456/_z_456d.py)
- [`_z_456e.py`](../../solve/456/_z_456e.py)
- [`_z_456f.py`](../../solve/456/_z_456f.py)
- [`_z_456g.py`](../../solve/456/_z_456g.py)
- [`_z_456h.py`](../../solve/456/_z_456h.py)
- [`_z_456i.py`](../../solve/456/_z_456i.py)
- [`_z_456j.py`](../../solve/456/_z_456j.py)
- [`_z_456k.py`](../../solve/456/_z_456k.py)
- [`_z_456l.py`](../../solve/456/_z_456l.py)
- [`_z_456m.py`](../../solve/456/_z_456m.py)
