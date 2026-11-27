# asm4

**Catégorie** : Reverse Engineering · **Challenge** : #5 · **Résolu le** : 2026-11-24

## Énoncé

> What will asm4("academy_7749b") return? Submit the flag as a hexadecimal value (starting with '0x'). NOTE: Your submission for this question will NOT be in the normal flag format. [Source](https://challenge-files.cylabacademy.net/library/cd3273ea6a389e14e06d8ae09234577faaabb1148e0f17b8e927d63af05fba8e/test.S)

## Résolution

Méthode : **lecture d'assemblee**.

`asm4` initialise `acc = 0x26d` puis, pour i de 1 a len-2, ajoute `(s[i]-s[i-1]) + (s[i+1]-s[i])`. La somme est **telescopique** : il reste `acc + s[len-2] + s[len-1] - s[0] - s[1]` = 621 + 57 + 98 - 97 - 99 = 580 = 0x244.

## Flag

```
0x244
```
