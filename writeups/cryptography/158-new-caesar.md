# New Caesar

**Catégorie** : Cryptography · **Challenge** : #158 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **base16 + cesar sur 16 caracteres**.

La source montre : alphabet limite a `abcdefghijklmnop` (16), `b16_encode` coupe chaque octet en deux nibbles, puis `shift` ajoute la valeur d'une cle d'UN caractere modulo 16. Brute force des 16 cles -> `m` donne `et_tu?_a91448ca`.

## Flag

```
academy{et_tu?_a91448ca}
```

## Ce qu'il faut retenir

—
