# Commitment Issues

**Catégorie** : Général Skills · **Challenge** : #411 · **Résolu le** : 2026-11-23

## Énoncé

> I accidentally wrote the flag down. Good thing I deleted it!
>
> You download the challenge files here:
>
> - [challenge.zip](https://challenge-files.cylabacademy.net/library/cbe1762032f789800c389f1c9a26f7a5f1cbe8dfb738ee1fede29023a3981b18/challenge.zip)

## Résolution

Méthode : **git log -p (fichier supprime)**.

Le depot contient deux commits : `create flag` puis `remove sensitive info`. Le second supprime le fichier, mais `git log --all -p` rejoue le diff et le flag reste dans l'historique. Piege : le zip s'extrait dans un sous-dossier `drop-in/` — lancer git dans le bon repertoire.

## Flag

```
academy{s@n1t1z3_f1ce74e2}
```
