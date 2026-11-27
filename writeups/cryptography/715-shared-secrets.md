# Shared Secrets

**Catégorie** : Cryptography · **Challenge** : #715 · **Résolu le** : 2026-11-23

## Énoncé

> A message was encrypted using a shared secret... but it looks like one side of the exchange leaked something. Can you piece together the secret and get the flag?
> Download the [message](https://challenge-files.cylabacademy.net/library/229381d5dd0dd4fa9da2439cb70d3b5dd39bc39c605506118af8c135142fa9f3/message.txt). And source [code](https://challenge-files.cylabacademy.net/library/229381d5dd0dd4fa9da2439cb70d3b5dd39bc39c605506118af8c135142fa9f3/encryption.py)

## Résolution

Méthode : **diffie-hellman + XOR octet**.

Le transcript donne `g=2`, `p`, `A` et **b** (le secret du client a fuite). `shared = pow(A, b, p)`, puis le flag est chiffré par XOR avec `shared % 256`. Le `enc` est en hex : on déchiffre octet par octet.

## Flag

```
academy{dh_s3cr3t_5d9c8fbe}
```
