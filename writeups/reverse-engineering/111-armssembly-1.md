# ARMssembly 1

**Catégorie** : Reverse Engineering · **Challenge** : #111 · **Résolu le** : 2026-11-23

## Énoncé

> For what argument does this program print "win"?
>
> Flag format: academy{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be academy{0055aabb})
> Variables: a = 60, b = 0, c = 3
>
> File: [chall_1.S](https://challenge-files.cylabacademy.net/library/faf1dc0995a3edfb49290cb451b6c151521d8979a6b05fb4220e313b49a709a1/chall_1.S)

## Résolution

Méthode : **résolution algebrique de l'assembleur ARM**.

`func(x)` calcule `((60 << 0) / 3) - x`. main affiche "You win!" si le resultat est 0, donc x = 20 = 0x14, soit `academy{00000014}` (32 bits, minuscules).

## Flag

```
academy{00000014}
```
