# Bbbbloat

**Catégorie** : Reverse Engineering · **Challenge** : #255 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **cmp immediat dans le desassemblage**.

Le binaire demande un nombre. En desassemblant apres le `scanf`, on trouve `cmp eax,0x86187` : c'est le nombre favori (549255). Il imprime alors le flag.

## Flag

```
academy{cu7_7h3_bl047_d67f6a67}
```

## Ce qu'il faut retenir

—
