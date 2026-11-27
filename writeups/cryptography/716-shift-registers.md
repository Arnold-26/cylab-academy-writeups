# shift registers

**Catégorie** : Cryptography · **Challenge** : #716 · **Résolu le** : 2026-11-23

## Énoncé

> I learned about lfsr today in school so i decided to implement it in my program. It must be safe right?
> [chall.py](https://challenge-files.cylabacademy.net/library/d252af24c7e168d84bf90bbeeceb0c43186cee51e7a92545e0f3ad799c3eedaf/chall.py)
> [output.txt](https://challenge-files.cylabacademy.net/library/d252af24c7e168d84bf90bbeeceb0c43186cee51e7a92545e0f3ad799c3eedaf/output.txt)

## Résolution

Méthode : **bruteforce LFSR 8 bits**.

`key = bytes_to_long(get_random_bytes(126))` mais le LFSR est initialise avec `key & 0xFF` : seuls **8 bits** de la clé comptent. On essaie les 256 etats initiaux et on XOR le chiffre ; le seed 162 donne le flag.

## Flag

```
academy{l1n3ar_f33dback_sh1ft_r3g}
```
