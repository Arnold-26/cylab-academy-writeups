# shift registers

**Catégorie** : Cryptography · **Challenge** : #716 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **bruteforce LFSR 8 bits**.

`key = bytes_to_long(get_random_bytes(126))` mais le LFSR est initialise avec `key & 0xFF` : seuls **8 bits** de la cle comptent. On essaie les 256 etats initiaux et on XOR le chiffre ; le seed 162 donne le flag.

## Flag

```
academy{l1n3ar_f33dback_sh1ft_r3g}
```
