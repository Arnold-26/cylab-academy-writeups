# transposition-trial

**Catégorie** : Cryptography · **Challenge** : #312 · **Résolu le** : 2026-11-23

## Énoncé

> Our data got corrupted on the way here. Luckily, nothing got replaced, but every block of 3 got scrambled around! The first word seems to be three letters long, maybe you can use that to recover the rest of the message.
> Download the corrupted message [here](https://challenge-files.cylabacademy.net/library/575d166ae8e15aa3d7119731bdfb61feb9682e987d146d02fa3b47dde75d596a/message.txt).

## Résolution

Méthode : **transposition par blocs de 3**.

Le texte est corrompu par blocs de 3 caractères permutes. Les 6 permutations possibles sont testees ; `(2,0,1)` donne le texte lisible `The flag is academy{...}`.

## Flag

```
academy{7R4N5P051N6_15_3XP3N51V3_27F6D45C}
```
