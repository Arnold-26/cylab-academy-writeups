# XtraORdinary

**Catégorie** : Cryptography · **Challenge** : #208 · **Résolu le** : 2026-11-23

## Énoncé

> Check out my new, never-before-seen method of encryption! I totally invented it myself. I added so many for loops that I don't even know what it does. It's extraordinarily secure!

## Résolution

Méthode : **XOR avec chaînes connues + clé répétée**.

Le flag est XORe avec une clé secrete, puis avec 10 chaînes connues un nombre aléatoire de fois. Comme XOR est involutif, chaque chaîne compte modulo 2 -> 2^10 combinaisons (32 uniques car les 'ever' sont identiques). Pour chaque candidat, on suppose le préfixe `picoCTF{`, on en deduit une clé périodique (ici `Africa!`, longueur 7) et on déchiffre.

## Flag

```
picoCTF{w41t_s0_1_d1dnt_1nv3nt_x0r???}
```
