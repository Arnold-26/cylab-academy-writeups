# john_pollard

**Catégorie** : Cryptography · **Challenge** : #6 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **factorisation RSA (Pollard rho)**.

Le certificat X.509 a un module RSA de **53 bits** seulement (`4966306421059967`). Pollard rho le factorise instantanement en `67867967 x 73176001` (deux premiers). Le flag est la paire de facteurs.

## Flag

```
academy{73176001,67867967}
```

## Ce qu'il faut retenir

—
