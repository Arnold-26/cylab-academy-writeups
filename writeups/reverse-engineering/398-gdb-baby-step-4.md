# GDB baby step 4

**Catégorie** : Reverse Engineering · **Challenge** : #398 · **Résolu le** : 2026-11-23

## Énoncé

> `main` calls a function that multiplies `eax` by a constant. The flag for this
> challenge is that constant in decimal base. If the constant you find is 0x1000,
> the flag will be `academy{4096}`.
> Debug [this](https://challenge-files.cylabacademy.net/library/5c4fe0af7766d02123d4ebea4a32b3b461fc6c5947049092d61d47518f298068/debugger0_d).

## Résolution

Méthode : **imul eax,eax,0x3269**.

Technique : imul eax,eax,0x3269.

## Flag

```
academy{12905}
```
