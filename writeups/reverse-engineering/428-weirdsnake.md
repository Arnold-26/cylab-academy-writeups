# weirdSnake

**Catégorie** : Reverse Engineering · **Challenge** : #428 · **Résolu le** : 2026-11-23

## Énoncé

> I have a friend that enjoys coding and he hasn't stopped talking about a snake recently
>
> He left this [file](https://challenge-files.cylabacademy.net/library/9945a1a2554281f0f3cc1c794ca01791743456f2f7182b049c7434cac253c06d/snake) on my computer and dares me to uncover a secret phrase from it. Can you assist?

## Résolution

Méthode : **bytecode Python -> XOR**.

Le fichier `snake` est un **disassemblee de bytecode Python**. On y lit `input_list = (21, 60, ...)` et la construction de `key_str` : 'J' -> '_J' -> '_Jo' -> '_Jo3' -> 't_Jo3'. Un XOR cyclique de input_list avec la clé donne le flag.

## Flag

```
academy{N0t_sO_coNfus1ng_sn@ke_0ed60894}
```
