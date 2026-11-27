# Custom encryption

**Catégorie** : Cryptography · **Challenge** : #412 · **Résolu le** : 2026-11-23

## Énoncé

> Can you get sense of this code file and write the function that will decode the given encrypted file content.
>
> Find the encrypted file here [flag_info](https://challenge-files.cylabacademy.net/library/98cdf4861b6c249cc4b06324768d9fbe57cc1cd8512fce4d03595601f380fc0f/enc_flag) and [code file](https://challenge-files.cylabacademy.net/library/98cdf4861b6c249cc4b06324768d9fbe57cc1cd8512fce4d03595601f380fc0f/custom_encryption.py) might be good to analyze and get the flag.

## Résolution

Méthode : **diffie-hellman + xor + division**.

Le script fait un échange Diffie-Hellman (`p=97, g=31, a, b`) puis `encrypt` multiplie chaque ord par `key*311`. On retrouve le semi-chiffre par division entiere, puis on inverse le `dynamic_xor_encrypt` (XOR avec `text_key='trudeau'` + reverse).

## Flag

```
academy{custom_d2cr0pt6d_203edf41}
```
