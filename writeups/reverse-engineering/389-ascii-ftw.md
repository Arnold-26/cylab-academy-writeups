# ASCII FTW

**Catégorie** : Reverse Engineering · **Challenge** : #389 · **Résolu le** : 2026-11-23

## Énoncé

> This program has constructed the flag using hex ascii values. Identify the flag text by disassembling the program.
> You can download the file from [here](https://challenge-files.cylabacademy.net/library/60ac124e46a3c8894d62ac83ba929cdebd78f28658dc91611d4aae76ad1cb41a/asciiftw).

## Résolution

Méthode : **desassemblage (mov immediats)**.

`objdump -d -M intel` sur main montre une serie de `mov BYTE PTR [rbp-0x..], 0x..` : chaque octet est une lettre du flag en ASCII. On lit la sequence et on decode.

## Flag

```
academy{ASCII_IS_EASY_AC3E0C8C}
```
