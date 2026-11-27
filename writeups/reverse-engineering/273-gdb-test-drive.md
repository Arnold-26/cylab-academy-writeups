# GDB Test Drive

**Catégorie** : Reverse Engineering · **Challenge** : #273 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **saut par-dessus le sleep**.

Le binaire fait un `sleep` avant d'afficher le flag. On casse a `main+99`, on lance, puis `jump *(main+104)` saute le sleep ; `continue` affiche le flag.

## Flag

```
academy{d3bugg3r_dr1v3_d28daa02}
```

## Ce qu'il faut retenir

—
