# ARMssembly 1

**Catégorie** : Reverse Engineering · **Challenge** : #111 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **resolution algebrique de l'assembleur ARM**.

`func(x)` calcule `((60 << 0) / 3) - x`. main affiche "You win!" si le resultat est 0, donc x = 20 = 0x14, soit `academy{00000014}` (32 bits, minuscules).

## Flag

```
academy{00000014}
```

## Ce qu'il faut retenir

—
