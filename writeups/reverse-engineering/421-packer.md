# packer

**Catégorie** : Reverse Engineering · **Challenge** : #421 · **Résolu le** : 2026-11-23

## Énoncé

> Reverse this linux executable?
>
> [binary](https://challenge-files.cylabacademy.net/library/41031ff5dea80688db22b2a9cf75b4e8cfee92b35d3e107a6cb324126c7cc312/out)

## Résolution

Méthode : **upx -d puis strings hex**.

Le binaire est **UPX** : `upx -d out -o out.unpacked` le depaquette. Dans le binaire decompresse, le message de succes contient le flag en **hexadécimal** : `61636164656d797b...` se decode directement.

## Flag

```
academy{U9X_UnP4ck1N6_B1n4Ri3S_0fafb2d7}
```
