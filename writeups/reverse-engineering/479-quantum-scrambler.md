# Quantum Scrambler

**Catégorie** : Reverse Engineering · **Challenge** : #479 · **Résolu le** : 2026-11-23

## Énoncé

> We invented a new cypher that uses "quantum entanglement" to encode the flag. Do
> you have what it takes to decode it?

## Résolution

Méthode : **inversion tracee du scramble**.

`scramble(L)` fait `A[i-2] += A.pop(i-1)` puis `A[i-1].append(A[:i-2])` : les slices ajoutees creent des copies imbriquees qui font exploser la taille. Pour inverser, il faut tracer chaque opération pendant un scramble factice de même longueur (les longueurs ne dependent pas des valeurs), puis rejouer les opérations à l'envers : retirer le slice ajoute, puis re-inserer les n elements poppes à la position i-1.

## Flag

```
academy{python_is_weirdade7472a}
```
