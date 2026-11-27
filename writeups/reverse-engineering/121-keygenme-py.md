# keygenme-py

**Catégorie** : Reverse Engineering · **Challenge** : #121 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **sha256 tronque**.

Le flag est `academy{1n_7h3_kk3y_of_` + 8 caracteres + `}`. `check_key` compare chaque caractere dynamique a `sha256("MILLER").hexdigest()[i]` avec les indices 4,5,3,6,2,7,1,8 dans cet ordre. On recalcule le hash et on assemble.

## Flag

```
academy{1n_7h3_kk3y_of_9edf443b}
```

## Ce qu'il faut retenir

—
