# Ready Gladiator 1

**Catégorie** : Reverse Engineering · **Challenge** : #369 · **Résolu le** : 2026-11-23

## Énoncé

> Can you make a CoreWars warrior that wins?

## Résolution

Méthode : **Dwarf bomber**.

CoreWars contre l'Imp (`mov 0,1`). Le **Dwarf** (`add #4,3 / mov 2,@2 / jmp -2`) bombe la mémoire par pas de 4 et finit par toucher l'Imp : 24 victoires sur 100, suffisant pour valider le challenge.

## Flag

```
academy{1mp_1n_7h3_cr055h41r5_87c8ae6a}
```
