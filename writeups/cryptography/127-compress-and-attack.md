# Compress and Attack

**Catégorie** : Cryptography · **Challenge** : #127 · **Résolu le** : 2026-11-23

## Énoncé

> Your goal is to find the flag.

## Résolution

Méthode : **oracle de compression (CRIME)**.

Le service compresse (`zlib`) le flag concatene a notre entrée puis chiffre en AES-CTR, et renvoie la taille. C'est un **oracle de compression** : plus notre entrée partage de préfixe avec le flag, plus le resultat compresse est court. En testant chaque caractère et en gardant celui qui minimise la longueur, on reconstruit le flag lettre par lettre.

## Flag

```
academy{sheriff_you_solved_the_crime}
```
