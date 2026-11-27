# Blame Game

**Catégorie** : Général Skills · **Challenge** : #405 · **Résolu le** : 2026-11-23

## Énoncé

> Someone's commits seems to be preventing the program from working. Who is it?
>
> You can download the challenge files here:
>
> - [challenge.zip](https://challenge-files.cylabacademy.net/library/5b75c6f8e836ba15c383c89de1c30922154130705b717ae60658810cc0bd5ffe/challenge.zip)

## Résolution

Méthode : **git log -p (historique complet)**.

Le depot à des dizaines de commits 'important business work'. Le flag n'est pas dans le fichier courant mais dans l'**historique** : `git log --all -p | grep academy`. Piege : le zip s'extrait dans `drop-in/`.

## Flag

```
academy{@sk_th3_1nt3rn_43769efb}
```
