# endianness

**Catégorie** : General Skills · **Challenge** : #414 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **conversion little/big endian**.

Service nc : il donne un mot de 5 lettres, demande sa representation **little endian** (octets en ordre inverse, hex) puis **big endian** (hex dans l'ordre). `''.join(f'{ord(c):02X}' for c in reversed(word))` puis sans `reversed`.

## Flag

```
academy{3ndi4n_sw4p_su33ess_5da2acc3}
```
