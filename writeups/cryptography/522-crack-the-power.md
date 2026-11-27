# Crack the Power

**Catégorie** : Cryptography · **Challenge** : #522 · **Résolu le** : 2026-11-23

## Énoncé

> We received an encrypted message. The modulus is built from primes large enough that factoring them isn’t an option, at least not today. See if you can make sense of the numbers and reveal the flag.
> Download the [message](https://challenge-files.cylabacademy.net/library/045cb85019ff34b1046bdea29511114f0f635e533109dc1b88bb3bc42b39658d/message.txt).

## Résolution

Méthode : **racine e-ieme exacte**.

`e = 20` et le message est court : `m^20` reste **plus petit que n**, donc on peut prendre la racine 20-ieme entiere de `c` directement, sans factoriser n.

## Flag

```
academy{t1ny_e_0afbc467}
```
