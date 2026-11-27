# rsa_oracle

**Catégorie** : Cryptography · **Challenge** : #422 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **oracle RSA + blindage + openssl**.

L'oracle expose E (chiffrer) et D (dechiffrer) mais **refuse** le chiffre du mot de passe. Etape 1 : recuperer `n` en chiffrant `2` et `3` — l'oracle encode l'entree en bytes (donc m=0x32 et 0x33), et `n = gcd(50^65537 - c2, 51^65537 - c3)`. Etape 2 : blindage multiplicatif `c' = c * 2^e mod n`, l'oracle rend `2m`, on divise. Etape 3 : le mot de passe obtenu dechiffre `secret.enc` (OpenSSL `Salted__`) avec `openssl enc -d -aes-256-cbc` **sans** `-pbkdf2`.

## Flag

```
academy{su((3ss_(r@ck1ng_r3@_20373ec2}
```

## Ce qu'il faut retenir

—
