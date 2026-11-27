# Virtual Machine 1

**Catégorie** : Reverse Engineering · **Challenge** : #386 · **Résolu le** : 2026-11-24

## Énoncé

> nc xebec.cylabacademy.net 12383

## Résolution

Méthode : **ratio compose d'engrenages (7*191*7)**.

Meme principe que VM0 mais avec un **train d'engrenages bevel a 3 etages** : le ratio compose vaut 7 x 191 x 7 = **9359**. Le service demande « If the input to the machine is <n>, what is the output? » : il faut multiplier l'entier fourni par 9359 et renvoyer le resultat. Le modele `.dae` contient les pieces LEGO (3647=8 dents, 3648b=16, 3649/4019=24, 32270=12, plus les axes 3704/3707/32073/4519) ; la difficulte est de ne pas oublier l'etage intermediaire cache derriere le carter, sinon on multiplie deux ratios au lieu de trois.

## Flag

```
academy{m0r3_g34r5_3g4d_c3dc2830}
```

## Scripts

- [`solve.py`](../../solve/386/solve.py)
- *4 variantes intermediaires dans `solve/386/archive/`*
