# rsa_oracle

**Catégorie** : Cryptography · **Challenge** : #422 · **Résolu le** : 2026-11-23

## Énoncé

> Can you abuse the oracle?
>
> An attacker was able to intercept communications between a bank and a fintech company. They managed to get the [message](https://challenge-files.cylabacademy.net/library/0d44678c5a09bacc6d0ff4226f7ed3e66bc9f62c37de7a58fc588bad8eb76f88/secret.enc) (ciphertext) and the [password](https://challenge-files.cylabacademy.net/library/0d44678c5a09bacc6d0ff4226f7ed3e66bc9f62c37de7a58fc588bad8eb76f88/password.enc) that was used to encrypt the message.

## Résolution

Méthode : **oracle RSA + blindage + openssl**.

L'oracle expose E (chiffrer) et D (déchiffrer) mais **refuse** le chiffre du mot de passe. Étape 1 : récupérer `n` en chiffrant `2` et `3` — l'oracle encode l'entrée en bytes (donc m=0x32 et 0x33), et `n = gcd(50^65537 - c2, 51^65537 - c3)`. Étape 2 : blindage multiplicatif `c' = c * 2^e mod n`, l'oracle rend `2m`, on divise. Étape 3 : le mot de passe obtenu déchiffre `secret.enc` (OpenSSL `Salted__`) avec `openssl enc -d -aes-256-cbc` **sans** `-pbkdf2`.

## Flag

```
academy{su((3ss_(r@ck1ng_r3@_20373ec2}
```
