# Transformation

**Catégorie** : Reverse Engineering · **Challenge** : #104 · **Résolu le** : 2026-11-23

## Énoncé

> I wonder what this really is...
> [enc](https://challenge-files.cylabacademy.net/library/a66c4924e86aac8724fa7824ba587586d87c47254dc421afc3abeef71a039120/enc)
>
> ```
> ''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])
> ```

## Résolution

Méthode : **decodage 16 bits**.

Le fichier `enc` contient un caractère par paire d'octets du flag : `chr((ord(flag[i]) << 8) + ord(flag[i+1]))`. Pour decoder, on lit le fichier en **UTF-8** et on sépare chaque code en deux octets (octet haut, octet bas).

## Flag

```
academy{16_bits_inst34d_of_8_790ba37e}
```
