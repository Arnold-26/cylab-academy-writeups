# NSA Backdoor

**Catégorie** : Cryptography · **Challenge** : #283 · **Résolu le** : 2026-11-23

## Énoncé

> I heard someone has been sneakily installing backdoors in open-source
> implementations of Diffie-Hellman... I wonder who it could be... ;)
> - [gen.py](https://challenge-files.cylabacademy.net/library/3fc119584f6ac475413bc32771b3db55b6b09149979eacef24f15166ce454a9c/gen.py)
> - [output.txt](https://challenge-files.cylabacademy.net/library/3fc119584f6ac475413bc32771b3db55b6b09149979eacef24f15166ce454a9c/output.txt)

## Résolution

Méthode : **Pollard p-1 + Pohlig-Hellman + ordre de 3**.

Primes **smooth** (p-1 en facteurs de 16 bits) : Pollard p-1 avec B = 2^16 donne p. Le chiffre est `c = 3^FLAG mod n`, donc un **logarithme discret** ; l'ordre du groupe etant friable, Pohlig-Hellman + BSGS le resout. Piege : le logarithme n'est defini qu'à `ord(3)` pres, et `ord(3)` (2045 bits) est inférieur à `lcm(p-1,q-1)` — il faut reduire le resultat modulo l'ordre exact de 3 pour retrouver le flag (351 bits).

## Flag

```
academy{b3w4r3_0f_c0mp0s1t3_m0dul1_975c2a44}
```
