# NSA Backdoor

**Catégorie** : Cryptography · **Challenge** : #283 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **Pollard p-1 + Pohlig-Hellman + ordre de 3**.

Primes **smooth** (p-1 en facteurs de 16 bits) : Pollard p-1 avec B = 2^16 donne p. Le chiffre est `c = 3^FLAG mod n`, donc un **logarithme discret** ; l'ordre du groupe etant friable, Pohlig-Hellman + BSGS le resout. Piege : le logarithme n'est defini qu'a `ord(3)` pres, et `ord(3)` (2045 bits) est inferieur a `lcm(p-1,q-1)` — il faut reduire le resultat modulo l'ordre exact de 3 pour retrouver le flag (351 bits).

## Flag

```
academy{b3w4r3_0f_c0mp0s1t3_m0dul1_975c2a44}
```
