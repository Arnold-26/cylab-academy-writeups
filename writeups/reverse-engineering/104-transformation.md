# Transformation

**Catégorie** : Reverse Engineering · **Challenge** : #104 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **decodage 16 bits**.

Le fichier `enc` contient un caractere par paire d'octets du flag : `chr((ord(flag[i]) << 8) + ord(flag[i+1]))`. Pour decoder, on lit le fichier en **UTF-8** et on separe chaque code en deux octets (octet haut, octet bas).

## Flag

```
academy{16_bits_inst34d_of_8_790ba37e}
```
