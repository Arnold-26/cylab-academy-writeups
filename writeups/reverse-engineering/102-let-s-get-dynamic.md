# Let's get dynamic

**Catégorie** : Reverse Engineering · **Challenge** : #102 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **reconstruction du flag a l'execution**.

Le binaire stocke **deux tableaux de 48 octets** (6 qwords chacun) et calcule pour chaque indice `flag[i] = A[i] ^ B[i] ^ i ^ 19`. Il suffit d'extraire les constantes `movabsq` et d'appliquer la formule.

## Flag

```
academy{dyn4m1c_4n4ly1s_1s_5up3r_us3ful_0c8f18c}
```

## Ce qu'il faut retenir

—
