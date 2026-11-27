# XtraORdinary

**Catégorie** : Cryptography · **Challenge** : #208 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **XOR avec chaines connues + cle repetee**.

Le flag est XORe avec une cle secrete, puis avec 10 chaines connues un nombre aleatoire de fois. Comme XOR est involutif, chaque chaine compte modulo 2 -> 2^10 combinaisons (32 uniques car les 'ever' sont identiques). Pour chaque candidat, on suppose le prefixe `picoCTF{`, on en deduit une cle periodique (ici `Africa!`, longueur 7) et on dechiffre.

## Flag

```
picoCTF{w41t_s0_1_d1dnt_1nv3nt_x0r???}
```
