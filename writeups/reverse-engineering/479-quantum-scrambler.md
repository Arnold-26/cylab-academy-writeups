# Quantum Scrambler

**Catégorie** : Reverse Engineering · **Challenge** : #479 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **inversion tracee du scramble**.

`scramble(L)` fait `A[i-2] += A.pop(i-1)` puis `A[i-1].append(A[:i-2])` : les slices ajoutees creent des copies imbriquees qui font exploser la taille. Pour inverser, il faut tracer chaque operation pendant un scramble factice de meme longueur (les longueurs ne dependent pas des valeurs), puis rejouer les operations a l'envers : retirer le slice ajoute, puis re-inserer les n elements poppes a la position i-1.

## Flag

```
academy{python_is_weirdade7472a}
```

## Ce qu'il faut retenir

—
