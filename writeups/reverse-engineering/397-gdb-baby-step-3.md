# GDB baby step 3

**Catégorie** : Reverse Engineering · **Challenge** : #397 · **Résolu le** : 2026-11-23

## Énoncé

> Now for something a little different. `0x2262c96b` is loaded into memory in the
> `main` function. Examine byte-wise the memory that the constant is loaded in by
> using the GDB command `x/4xb addr`. The flag is the four bytes as they are
> stored in memory. If you find the bytes `0x11 0x22 0x33 0x44` in the memory
> location, your flag would be: `academy{0x11223344}`.
> Debug [this](https://challenge-files.cylabacademy.net/library/5eb60afe8ad6df789decfd9d5af027dc8184bfbc20e953f76ed38bd9ce3d9582/debugger0_c).

## Résolution

Méthode : **octets little-endian de 0x2262c96b**.

Technique : octets little-endian de 0x2262c96b.

## Flag

```
academy{0x6bc96222}
```
