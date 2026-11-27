# b00tl3gRSA2

**Catégorie** : Cryptography · **Challenge** : #2 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **e et d inverses**.

Le service affiche un `e` de 1024 bits : c'est en realite **d**. Le vrai exposant public est petit. On essaie `pow(c, 3/5/17/257/65537, n)` : **65537** donne le flag.

## Flag

```
academy{bad_1d3a5_1972548}
```
