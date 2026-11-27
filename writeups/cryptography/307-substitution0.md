# substitution0

**Catégorie** : Cryptography · **Challenge** : #307 · **Résolu le** : 2026-11-23

## Énoncé

> A message has come in but it seems to be all scrambled. Luckily it seems to
> have the key at the beginning. Can you crack this substitution cipher?
> Download the message [here](https://challenge-files.cylabacademy.net/library/c81cd186dacb4ad82560df3b81fe365fc1c38a1c7dca9a73a9604c5345ab4473/message.txt).

## Résolution

Méthode : **substitution monoalphabetique**.

La première ligne du fichier est l'alphabet de substitution (26 lettres) : A->D, B->J, C->H... Pour déchiffrer, chercher chaque lettre chiffree dans la clé et prendre la lettre de l'alphabet standard au même index. Le texte clair est un extrait de Poe et le flag y figure en clair.

## Flag

```
academy{5UB5717U710N_3V0LU710N_6A8C4822}
```
