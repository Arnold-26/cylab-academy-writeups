# Neuron Meet 0

**Catégorie** : Artificial Intelligence · **Challenge** : #771 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **bissection du seuil + sequence ASCII**.

Un perceptron 1D repond `w*x + b >= 0`. En bissectant sur [-10, 10] on trouve le seuil, puis on choisit 8 valeurs distinctes (pas de repetition consecutive) pour produire la sequence `01110000` = ASCII 'p'.

## Flag

```
academy{n3ur0n_m3t_486f8b0e}
```
