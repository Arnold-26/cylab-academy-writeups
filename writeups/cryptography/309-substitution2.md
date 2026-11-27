# substitution2

**Catégorie** : Cryptography · **Challenge** : #309 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **hill-climbing quadgrammes + alignement**.

Substitution monoalphabetique sans ponctuation. J'ai ecrit un solveur par hill-climbing sur des quadgrammes extraits de `/usr/share/dict/words`, puis affine le mapping par alignement avec le texte anglais reconnu. Le clair se termine par « the flag is academy{...} » en leetspeak.

## Flag

```
academy{N6R4M_4N41Y515_15_73D10U5_9F106B2E}
```

## Ce qu'il faut retenir

—
