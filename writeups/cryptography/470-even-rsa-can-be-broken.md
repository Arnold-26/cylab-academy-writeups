# EVEN RSA CAN BE BROKEN???

**Catégorie** : Cryptography · **Challenge** : #470 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **N pair -> p=2**.

Le service donne N, e et le chiffre. **N est pair** : donc p=2 et q=N/2. `phi=(2-1)(q-1)`, `d=e^-1 mod phi`, `m=c^d mod N`. Aucune factorisation necessaire.

## Flag

```
academy{tw0_1$_pr!m3cfb893a9}
```

## Ce qu'il faut retenir

—
