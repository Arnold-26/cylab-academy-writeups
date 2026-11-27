# Custom encryption

**Catégorie** : Cryptography · **Challenge** : #412 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **diffie-hellman + xor + division**.

Le script fait un echange Diffie-Hellman (`p=97, g=31, a, b`) puis `encrypt` multiplie chaque ord par `key*311`. On retrouve le semi-chiffre par division entiere, puis on inverse le `dynamic_xor_encrypt` (XOR avec `text_key='trudeau'` + reverse).

## Flag

```
academy{custom_d2cr0pt6d_203edf41}
```

## Ce qu'il faut retenir

—
