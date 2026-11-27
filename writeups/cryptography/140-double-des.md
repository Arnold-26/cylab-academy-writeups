# Double DES

**Catégorie** : Cryptography · **Challenge** : #140 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **meet-in-the-middle sur 2DES**.

Les cles sont des nombres a **6 chiffres** (10^6 possibilites). Attaque **meet-in-the-middle** : on chiffre un bloc clair connu avec les 10^6 cles k1, on stocke le resultat, puis on dechiffre le bloc chiffre avec les 10^6 cles k2 et on cherche une collision. Le flag n'est pas au format standard (simple hex).

## Flag

```
b8877408ec959ddfda7726f4986b52f5
```

## Ce qu'il faut retenir

—
