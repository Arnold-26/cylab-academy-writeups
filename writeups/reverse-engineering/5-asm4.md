# asm4

**Catégorie** : Reverse Engineering · **Challenge** : #5 · **Résolu le** : 2026-11-24

## Résolution

Méthode : **lecture d'assemblee**.

`asm4` initialise `acc = 0x26d` puis, pour i de 1 a len-2, ajoute `(s[i]-s[i-1]) + (s[i+1]-s[i])`. La somme est **telescopique** : il reste `acc + s[len-2] + s[len-1] - s[0] - s[1]` = 621 + 57 + 98 - 97 - 99 = 580 = 0x244.

## Flag

```
0x244
```
