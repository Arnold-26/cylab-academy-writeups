# weirdSnake

**Catégorie** : Reverse Engineering · **Challenge** : #428 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **bytecode Python -> XOR**.

Le fichier `snake` est un **disassemblee de bytecode Python**. On y lit `input_list = (21, 60, ...)` et la construction de `key_str` : 'J' -> '_J' -> '_Jo' -> '_Jo3' -> 't_Jo3'. Un XOR cyclique de input_list avec la cle donne le flag.

## Flag

```
academy{N0t_sO_coNfus1ng_sn@ke_0ed60894}
```
