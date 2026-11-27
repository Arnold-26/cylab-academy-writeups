# Black Cobra Pepper

**Catégorie** : Cryptography · **Challenge** : #701 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **AES lineaire -> algebre GF(2)**.

Dans `chall.py`, `sub_bytes` et `rcon` sont des **identites** : le chiffrement devient affine en la cle. Avec une paire clair/chiffre connue (`randomdata111111`), on calcule `F(0)` puis les 128 colonnes de la matrice lineaire `F(e_i) xor F(0)`, et on resout le systeme 128x128 sur GF(2). Cle trouvee : `a1a1a1a1b2b2b2b2c3c3c3c3d4d4d4d4`, puis on inverse les rounds pour dechiffrer.

## Flag

```
academy{spi1cy!}
```

## Ce qu'il faut retenir

—
