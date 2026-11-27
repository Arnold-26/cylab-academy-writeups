# substitution1

**Catégorie** : Cryptography · **Challenge** : #308 · **Résolu le** : 2026-11-23

## Énoncé

> A second message has come in the mail, and it seems almost identical to the first one. Maybe the same thing will work again.
> Download the message [here](https://challenge-files.cylabacademy.net/library/2b9afd354b9804667c07bd1cddecd56fa43db5878bca2dbe74c87dff1344e5c6/message.txt).

## Résolution

Méthode : **substitution monoalphabetique**.

Chiffre de substitution monoalphabetique. On derive le mapping depuis les mots courants (`CTFs`, `short`, `the`, `flag`) et depuis le format `academy{}`, puis on decode tout le message : le flag y figure en clair à la fin.

## Flag

```
academy{FR3QU3NCY_4774CK5_4R3_C001_0532A335}
```
