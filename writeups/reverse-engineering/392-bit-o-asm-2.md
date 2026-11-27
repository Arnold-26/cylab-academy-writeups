# Bit-O-Asm-2

**Catégorie** : Reverse Engineering · **Challenge** : #392 · **Résolu le** : 2026-11-23

## Énoncé

> Can you figure out what is in the `eax` register? Put your answer in the
> academy flag format: `academy{n}` where `n` is the contents of the `eax`
> register in the decimal number base. If the answer was `0x11` your flag would
> be `academy{17}`.
> Download the assembly dump [here](https://challenge-files.cylabacademy.net/library/0325d59cb3b29a78bb7872b19f37856d51973b33085362dd4fe5f4cbe7aef80c/disassembler-dump0_b.txt).

## Résolution

Méthode : **mov [rbp-4],0x9fe1a puis mov eax**.

Technique : mov [rbp-4],0x9fe1a puis mov eax.

## Flag

```
academy{654874}
```
