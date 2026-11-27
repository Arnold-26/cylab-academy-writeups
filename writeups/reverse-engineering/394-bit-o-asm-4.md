# Bit-O-Asm-4

**Catégorie** : Reverse Engineering · **Challenge** : #394 · **Résolu le** : 2026-11-23

## Énoncé

> Can you figure out what is in the `eax` register? Put your answer in the
> academy flag format: `academy{n}` where `n` is the contents of the `eax`
> register in the decimal number base. If the answer was `0x11` your flag would
> be `academy{17}`.
> Download the assembly dump [here](https://challenge-files.cylabacademy.net/library/b14a53c80d0f28fa842055ab567694917ef71b9f466545c3597aa8940284e212/disassembler-dump0_d.txt).

## Résolution

Méthode : **cmp 0x2710 puis sub 0x65**.

Technique : cmp 0x2710 puis sub 0x65.

## Flag

```
academy{654773}
```
