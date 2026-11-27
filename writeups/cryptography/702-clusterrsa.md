# ClusterRSA

**Catégorie** : Cryptography · **Challenge** : #702 · **Résolu le** : 2026-11-23

## Énoncé

> A message has been encrypted using RSA, but this time something feels... more crowded than usual. Can you decrypt it?
> Download the [message](https://challenge-files.cylabacademy.net/library/52b45696ca9bdbc76f3ae75fe4702b362c905813821075841f5e10f730d1db80/message.txt).

## Résolution

Méthode : **RSA multiprime (4 facteurs)**.

Le module `n` a **4 facteurs premiers** (RSA multiprime). factordb les donne, on calcule `phi = produit(p_i - 1)` puis `d = e^-1 mod phi` et on déchiffre.

## Flag

```
academy{mul71_rsa_411fc267}
```
