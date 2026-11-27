# OTP Implementation

**Catégorie** : Reverse Engineering · **Challenge** : #92 · **Résolu le** : 2026-11-24

## Énoncé

> Yay reversing!
>
> Relevant files: [otp](https://challenge-files.cylabacademy.net/library/ec233a396b9e59c9ae36797c2dc90a309c6e2166903052753d1c87d2f7449b56/otp) [enc_flag.txt](https://challenge-files.cylabacademy.net/library/ec233a396b9e59c9ae36797c2dc90a309c6e2166903052753d1c87d2f7449b56/enc_flag.txt)

## Résolution

Méthode : **inversion de jumble + XOR**.

`valid_char` n'accepte que des **chiffres hexadecimaux** ; la clé doit faire 100 caractères. `jumble` (c+=9 si c>0x60, puis `(c%16)*2`, +1 si >15) est une **bijection** sur {0-9a-f}, donc on inverse la somme cumulee mod 16 pour retrouver la clé (100 hex = 50 octets). Le flag est `enc_flag XOR key`.

## Flag

```
academy{cust0m_jumbl3s_4r3nt_4_g0Od_1d3A_731cd140}
```
