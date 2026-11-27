# Warmed Up

**Catégorie** : Général Skills · **Difficulté** : Easy · **Épreuve** : picoCTF 2019
**Challenge** : #58

## Énoncé

> What is 0x3D (base 16) in decimal (base 10)?

**Entrée** : —

## Résolution

Conversion directe : `int('3D', 16)` → **61**. Le hint confirme le format `academy{<réponse>}`.

## Flag

```
academy{61}
```

## Ce qu'il faut retenir

Les conversions de base sont la porte d'entrée : hex → décimal, décimal → binaire, hex → ASCII.
