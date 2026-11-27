# New Caesar

**Catégorie** : Cryptography · **Challenge** : #158 · **Résolu le** : 2026-11-23

## Énoncé

> We found a brand new type of encryption, can you break the secret code? (Wrap with academy{})
> cbdabldadbplblcnpfpnpapapecpcn [new_caesar.py](https://challenge-files.cylabacademy.net/library/a4ec3b6aac9c3a1d144a110e0d644cc768354f37cff6a97141bfdfa48b4433f8/new_caesar.py)

## Résolution

Méthode : **base16 + cesar sur 16 caractères**.

La source montre : alphabet limite à `abcdefghijklmnop` (16), `b16_encode` coupe chaque octet en deux nibbles, puis `shift` ajoute la valeur d'une clé d'UN caractère modulo 16. Brute force des 16 clés -> `m` donne `et_tu?_a91448ca`.

## Flag

```
academy{et_tu?_a91448ca}
```
