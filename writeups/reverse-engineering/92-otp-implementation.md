# OTP Implementation

**Catégorie** : Reverse Engineering · **Challenge** : #92 · **Résolu le** : 2026-11-24

## Résolution

Méthode : **inversion de jumble + XOR**.

`valid_char` n'accepte que des **chiffres hexadecimaux** ; la cle doit faire 100 caracteres. `jumble` (c+=9 si c>0x60, puis `(c%16)*2`, +1 si >15) est une **bijection** sur {0-9a-f}, donc on inverse la somme cumulee mod 16 pour retrouver la cle (100 hex = 50 octets). Le flag est `enc_flag XOR key`.

## Flag

```
academy{cust0m_jumbl3s_4r3nt_4_g0Od_1d3A_731cd140}
```
