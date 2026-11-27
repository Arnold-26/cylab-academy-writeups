# Binary Search

**Catégorie** : Général Skills · **Challenge** : #442 · **Résolu le** : 2026-11-23

## Énoncé

> Want to play a game? As you use more of the shell, you might be interested in how they work! Binary search is a classic algorithm used to quickly find an item in a sorted list. Can you find the flag? You'll have 1000 possibilities and only 10 guesses.
>
> Cyber security often has a huge amount of data to look through - from logs, vulnerability reports, and forensics. Practicing the fundamentals manually might help you in the future when you have to write your own tools!
>
> You can download the challenge files here:
>
> - [challenge.zip](https://challenge-files.cylabacademy.net/library/2aa8e819569293f8a4452ec0f51d581be44144f18e172a553fb1ae181c300786/challenge.zip)

## Résolution

Méthode : **SSH interactif : bissection**.

Jeu SSH : deviner un nombre entre 1 et 1000 en 10 essais. Bissection classique. Piege : parser la réponse en **delta** (nouvelle sortie), pas sur tout l'historique — sinon les anciens « Higher/Lower » faussent les bornes.

## Flag

```
academy{g00d_gu355_35a2fc47}
```
