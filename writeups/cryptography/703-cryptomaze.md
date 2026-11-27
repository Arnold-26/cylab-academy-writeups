# cryptomaze

**Catégorie** : Cryptography · **Challenge** : #703 · **Résolu le** : 2026-11-23

## Énoncé

> In this challenge, you are tasked with recovering a hidden flag that has been encrypted using a combination of Linear Feedback Shift Register (LFSR) and AES encryption. The LFSR is used to derive a key for AES encryption, making it crucial to understand its workings to decrypt the message.
>
> The flag has been stored in a file and encrypted. Your goal is to derive the key used for encryption from the LFSR state and taps provided in the output, and then decrypt the flag to retrieve it.
> Download the encrypted flag from [here](https://challenge-files.cylabacademy.net/library/333b94c0a78023326ff58adf696fe3f72d82666da8c1f5f43e685e43ea93f528/output.txt). which contains the following information:
>
> - The initial state of the LFSR
> - The taps used for the LFSR
> - The encrypted flag in hexadecimal format

## Résolution

Méthode : **LFSR -> clé AES**.

L'LFSR 64 bits (taps 63/61/60/58) est initialise avec l'etat donne. En generant 128 bits (décalage à gauche, bit de poids fort en premier), on obtient les 16 octets de clé AES `25ec96954d8bc45b2d7798a9fa0e1236` qui déchiffre le flag en AES-ECB.

## Flag

```
academy{scr8mbledt_flvg_b9b9bd42}
```
