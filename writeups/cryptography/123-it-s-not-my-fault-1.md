# It's Not My Fault 1

**Catégorie** : Cryptography · **Challenge** : #123 · **Résolu le** : 2026-11-25

## Énoncé

> fichier du challenge

## Résolution

Méthode : **attaque par reseau (lattice) sur un RSA avec exposant petit et message court**.

RSA avec un exposant d'chiffrement faible et un message court : le chiffre peut etre vu comme une combinaison lineaire de petits multiples du message. La resolution classique est une reduction de reseau (LLL) sur le treillis construit a partir de (e, n) et des chiffres. Technique : attaque par reseau (lattice) sur un RSA avec exposant petit et message court.

## Flag

```
academy{1_c4n'7_b3l13v3_17'5_n07_f4ul7_4774ck!!!}
```
