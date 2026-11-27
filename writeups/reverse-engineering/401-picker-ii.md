# Picker II

**Catégorie** : Reverse Engineering · **Challenge** : #401 · **Résolu le** : 2026-11-23

## Énoncé

> Can you figure out how this program works to get the flag?

## Résolution

Méthode : **contournement du filtre par concaténation**.

Le filtre `if 'win' in user_input` bloque le littoral. On passe `globals()['w'+'in']` : la chaîne 'win' n'apparait jamais dans l'entrée, mais l'evaluation produit bien `win()`.

## Flag

```
academy{f1l73r5_f41l_c0d3_r3f4c70r_m1gh7_5ucc33d_bd7d479d}
```
