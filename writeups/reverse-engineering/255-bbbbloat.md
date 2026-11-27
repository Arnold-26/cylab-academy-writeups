# Bbbbloat

**Catégorie** : Reverse Engineering · **Challenge** : #255 · **Résolu le** : 2026-11-23

## Énoncé

> Can you get the flag?
> Reverse engineer this [binary](https://challenge-files.cylabacademy.net/library/797bac900bf1cc3c89e751bd6e171896ab95b4527c97f9a7879276bba5661f80/bbbbloat).

## Résolution

Méthode : **cmp immediat dans le desassemblage**.

Le binaire demande un nombre. En desassemblant après le `scanf`, on trouve `cmp eax,0x86187` : c'est le nombre favori (549255). Il imprime alors le flag.

## Flag

```
academy{cu7_7h3_bl047_d67f6a67}
```
