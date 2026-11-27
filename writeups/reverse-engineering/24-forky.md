# Forky

**Catégorie** : Reverse Engineering · **Challenge** : #24 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **analyse de fork + mmap partage**.

Le programme `mmap` une zone **partagee** initialisee a 0x3B9ACA00 (1000000000), puis `fork()` 4 fois (16 processus). Chaque processus ajoute 0x499602D2 (1234567890) a la valeur partagee et passe le resultat a `doNothing`. Le dernier appel recoit la valeur apres les 16 additions : 1000000000 + 16*1234567890 mod 2^32 = 3573217056.

## Flag

```
academy{-721750240}
```

## Ce qu'il faut retenir

—
