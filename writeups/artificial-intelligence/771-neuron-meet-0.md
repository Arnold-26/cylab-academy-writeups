# Neuron Meet 0

**Catégorie** : Artificial Intelligence · **Challenge** : #771 · **Résolu le** : 2026-11-23

## Énoncé

> Probe a 1D perceptron over the network. Send it numbers and watch whether the neuron fires or not. Use those responses to figure out the decision boundary, then line up the last eight outputs to read the ASCII for `p` (`01110000`) and you'll earn the flag.

## Résolution

Méthode : **bissection du seuil + sequence ASCII**.

Un perceptron 1D répond `w*x + b >= 0`. En bissectant sur [-10, 10] on trouve le seuil, puis on choisit 8 valeurs distinctes (pas de repetition consecutive) pour produire la sequence `01110000` = ASCII 'p'.

## Flag

```
academy{n3ur0n_m3t_486f8b0e}
```
