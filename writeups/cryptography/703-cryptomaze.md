# cryptomaze

**Catégorie** : Cryptography · **Challenge** : #703 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **LFSR -> cle AES**.

L'LFSR 64 bits (taps 63/61/60/58) est initialise avec l'etat donne. En generant 128 bits (decalage a gauche, bit de poids fort en premier), on obtient les 16 octets de cle AES `25ec96954d8bc45b2d7798a9fa0e1236` qui dechiffre le flag en AES-ECB.

## Flag

```
academy{scr8mbledt_flvg_b9b9bd42}
```
