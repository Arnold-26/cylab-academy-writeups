# GDB baby step 1

**Catégorie** : Reverse Engineering · **Challenge** : #395 · **Résolu le** : 2026-11-23

## Énoncé

> Can you figure out what is in the `eax` register at the end of the `main`
> function? Put your answer in the academy flag format: `academy{n}` where `n` is
> the contents of the `eax` register in the decimal number base. If the answer
> was `0x11` your flag would be `academy{17}`.
> Disassemble [this](https://challenge-files.cylabacademy.net/library/03b038548e2a34973bde05a78fadc1f09467a1d03ffbfb9e4b48bd44e87c0e70/debugger0_a).

## Résolution

Méthode : **mov eax,0x86342**.

Technique : mov eax,0x86342.

## Flag

```
academy{549698}
```
