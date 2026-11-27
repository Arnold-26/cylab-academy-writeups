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

- [`solve.py`](../../solve/456/solve.py)
- *12 variantes intermediaires dans `solve/456/archive/`*
