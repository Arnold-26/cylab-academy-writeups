# substitution2

**Catégorie** : Cryptography · **Challenge** : #309 · **Résolu le** : 2026-11-23

## Énoncé

> It seems that another encrypted message has been intercepted. The encryptor
> seems to have learned their lesson though and now there isn't any punctuation!
> Can you still crack the cipher?
> Download the message [here](https://challenge-files.cylabacademy.net/library/696c6874056837b137b48e23a74d72e27d26def4454fdb690063e6baefa68124/message.txt).

## Résolution

Méthode : **hill-climbing quadgrammes + alignement**.

Substitution monoalphabetique sans ponctuation. J'ai écrit un solveur par hill-climbing sur des quadgrammes extraits de `/usr/share/dict/words`, puis affine le mapping par alignement avec le texte anglais reconnu. Le clair se termine par « the flag is academy{...} » en leetspeak.

## Flag

```
academy{N6R4M_4N41Y515_15_73D10U5_9F106B2E}
```
