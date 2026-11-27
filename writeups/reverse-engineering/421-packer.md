# packer

**Catégorie** : Reverse Engineering · **Challenge** : #421 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **upx -d puis strings hex**.

Le binaire est **UPX** : `upx -d out -o out.unpacked` le depaquette. Dans le binaire decompresse, le message de succes contient le flag en **hexadecimal** : `61636164656d797b...` se decode directement.

## Flag

```
academy{U9X_UnP4ck1N6_B1n4Ri3S_0fafb2d7}
```

## Ce qu'il faut retenir

—
