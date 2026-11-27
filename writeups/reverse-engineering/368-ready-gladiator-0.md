# Ready Gladiator 0

**Catégorie** : Reverse Engineering · **Challenge** : #368 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **warrior suicide**.

CoreWars : l'adversaire est l'Imp. Pour perdre a coup sur sans match nul, on soumet un warrior `dat 0,0` qui se detruit a la premiere instruction. Le serveur attend le code puis `end`.

## Flag

```
academy{h3r0_t0_z3r0_4m1r1gh7_327705a1}
```
