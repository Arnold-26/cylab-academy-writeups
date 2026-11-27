# Keygenme

**Catégorie** : Reverse Engineering · **Challenge** : #276 · **Résolu le** : 2026-11-24

## Énoncé

> Can you get the flag?
> Reverse engineer this [binary](https://challenge-files.cylabacademy.net/library/009110ef5a20e8a871ba44673564d33a64949e795c2e9b5f72536dc91278916f/keygenme).

## Résolution

Méthode : **extraction de la chaîne attendue par gdb**.

`keygenme` (ELF 64 PIE stripped) demande une licence. La fonction de vérification (0x1209) construit **le flag attendu sur la pile** : une serie de `movabs` partiellement chevauchants écrit `academy{H` a [rbp-0x90], `br1ng_y0H` a +8, `g_y0ur_0H` a +12 (ce qui ecrase et recolle en `br1ng_y0ur_0`), puis `wn_k3y_` a +20, donnant `academy{br1ng_y0ur_0wn_k3y_`. Ensuite l'entrée est hashee en MD5, convertie en hexa par `sprintf("%02x")`, et une partie de cet hexadécimal complète le flag. La comparaison finale (0x1442) est INLINE (boucle sur 36 caractères), donc les hooks LD_PRELOAD sur strcmp/memcmp ne declenchent rien. Il faut un **breakpoint gdb a 0x1442** (base PIE 0x555555554000 avec ASLR desactive, et entrée de 36 caractères sinon la fonction sort avant par un contrôle de longueur) puis `x/s $rbp-0x30` : la chaîne complète y est en clair.

## Flag

```
academy{br1ng_y0ur_0wn_k3y_bb724f88}
```

## Scripts

- [`solve.py`](../../solve/276/solve.py)
- *19 variantes intermediaires dans `solve/276/archive/`*
