# Virtual Machine 0

**Catégorie** : Reverse Engineering · **Challenge** : #385 · **Résolu le** : 2026-11-24

## Énoncé

> Can you crack this black box?
> We grabbed this design doc from enemy servers:
> [Download](https://challenge-files.cylabacademy.net/library/31a032462b68e74a4a4a303cccc1007b33149f2b232bec2c2c2a0840f3fbb3f1/Virtual-Machine-0.zip). We know that the rotation
> of the red axle is input and the rotation of the blue axle is output. The
> following input gives the flag as output: [Download](https://challenge-files.cylabacademy.net/library/31a032462b68e74a4a4a303cccc1007b33149f2b232bec2c2c2a0840f3fbb3f1/input.txt).

## Résolution

Méthode : **ratio d'engrenages LEGO -> hex -> ASCII**.

Le zip contient `Virtual-Machine-0.dae`, un modele **COLLADA** d'un train d'engrenages LEGO. Les geometries portent les numéros de pieces (`3004`, `3700`, `18651`, `44237`, `3647`, `6098`, `99008`, `3649`) : les engrenages sont 40 dents (rouge, entrée) et 8 dents (bleu, sortie), donc un **ratio 5:1**. `input.txt` donne un très grand entier ; multiplier par 5, convertir en hexadécimale puis decoder en ASCII donne directement le flag. Les autres ratios (1, 8, 40, 3, 4) donnent du bruit binaire.

## Flag

```
academy{g34r5_0f_m0r3_c95d6542}
```

## Scripts

- [`solve.py`](../../solve/385/solve.py)
- *2 variantes intermediaires dans `solve/385/archive/`*
