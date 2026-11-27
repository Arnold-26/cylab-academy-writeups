# Black Cobra Pepper

**Catégorie** : Cryptography · **Challenge** : #701 · **Résolu le** : 2026-11-23

## Énoncé

> i like peppers. (change!)
> [chall.py](https://challenge-files.cylabacademy.net/library/91e27d051904682244445ade0731de93da2d986ad610b747c9874bd821c2f89e/chall.py)
> [output.txt](https://challenge-files.cylabacademy.net/library/91e27d051904682244445ade0731de93da2d986ad610b747c9874bd821c2f89e/output.txt)

## Résolution

Méthode : **AES lineaire -> algebre GF(2)**.

Dans `chall.py`, `sub_bytes` et `rcon` sont des **identites** : le chiffrement devient affine en la clé. Avec une paire clair/chiffre connue (`randomdata111111`), on calcule `F(0)` puis les 128 colonnes de la matrice lineaire `F(e_i) xor F(0)`, et on resout le système 128x128 sur GF(2). Clé trouvee : `a1a1a1a1b2b2b2b2c3c3c3c3d4d4d4d4`, puis on inverse les rounds pour déchiffrer.

## Flag

```
academy{spi1cy!}
```
