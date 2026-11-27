# john_pollard

**Catégorie** : Cryptography · **Challenge** : #6 · **Résolu le** : 2026-11-23

## Énoncé

> Sometimes RSA certificates are breakable
> Certificates: [certificates](https://challenge-files.cylabacademy.net/library/3eb471c919b06785e45c7aeefd03b3f17638a2d190e3bc31ee3b5cec01832ac8/cert)

## Résolution

Méthode : **factorisation RSA (Pollard rho)**.

Le certificat X.509 à un module RSA de **53 bits** seulement (`4966306421059967`). Pollard rho le factorise instantanement en `67867967 x 73176001` (deux premiers). Le flag est la paire de facteurs.

## Flag

```
academy{73176001,67867967}
```
