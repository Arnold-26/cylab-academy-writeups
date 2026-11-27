# Shared Secrets

**Catégorie** : Cryptography · **Challenge** : #715 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **diffie-hellman + XOR octet**.

Le transcript donne `g=2`, `p`, `A` et **b** (le secret du client a fuite). `shared = pow(A, b, p)`, puis le flag est chiffre par XOR avec `shared % 256`. Le `enc` est en hex : on dechiffre octet par octet.

## Flag

```
academy{dh_s3cr3t_5d9c8fbe}
```

## Ce qu'il faut retenir

—
