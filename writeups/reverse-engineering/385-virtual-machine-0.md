# Virtual Machine 0

**Catégorie** : Reverse Engineering · **Challenge** : #385 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **ratio d'engrenages LEGO -> hex -> ASCII**.

Le zip contient `Virtual-Machine-0.dae`, un modele **COLLADA** d'un train d'engrenages LEGO. Les geometries portent les numeros de pieces (`3004`, `3700`, `18651`, `44237`, `3647`, `6098`, `99008`, `3649`) : les engrenages sont 40 dents (rouge, entree) et 8 dents (bleu, sortie), donc un **ratio 5:1**. `input.txt` donne un tres grand entier ; multiplier par 5, convertir en hexadecimale puis decoder en ASCII donne directement le flag. Les autres ratios (1, 8, 40, 3, 4) donnent du bruit binaire.

## Flag

```
academy{g34r5_0f_m0r3_c95d6542}
```

## Ce qu'il faut retenir

—

## Scripts

- [`solve.py`](../../solve/385/solve.py)
- *2 variantes intermediaires dans `solve/385/archive/`*
