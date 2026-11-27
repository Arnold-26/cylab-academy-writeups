# Dachshund Attacks

**Catégorie** : Cryptography · **Challenge** : #159 · **Résolu le** : 2026-11-23

## Énoncé

> What if $$d$$ is too small?

## Résolution

Méthode : **attaque de Wiener sur petit d**.

`d` est trop petit pour RSA : on developpe `e/n` en **fraction continue** et on teste chaque convergente `k/d`. Si `(e*d-1) % k == 0`, alors `phi = (e*d-1)/k`, `p+q = n - phi + 1`, et le discriminant `isqrt((p+q)^2 - 4n)` donne p et q. **Piege** : le service génère un nouveau triplet a CHAQUE connexion — il faut lire e, n et c dans la même session, sinon on déchiffre du bruit.

## Flag

```
academy{proving_wiener_ffef507}
```
