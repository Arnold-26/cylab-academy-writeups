# droids0

**Catégorie** : Reverse Engineering · **Challenge** : #11 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **XOR repetitif dans la lib native**.

La lib `libhellojni.so` contient 5 paires (cle, donnees) et 5 helpers (`marjoram`, `anise`, `oregano`, `sumac`, `pepper`) qui font un **XOR repetitif** `out[i] ^= key[i % keylen]`. Celle-ci : cle `notexist` (0x1a04) sur les donnees a 0x1a1a. Les autres challenges droids utilisent les autres paires de la meme lib.

## Flag

```
academy{a.moose.once.bit.my.sister}
```

## Ce qu'il faut retenir

—
