# Time Machine

**Catégorie** : Général Skills · **Challenge** : #425 · **Résolu le** : 2026-11-23

## Énoncé

> What was I last working on? I remember writing a note to help me remember...
>
> You can download the challenge files here:
>
> - [challenge.zip](https://challenge-files.cylabacademy.net/library/7272719b133b310bdbdcf12a116dd4499cd5d2c7247ee62e50f0a113aebfcdfb/challenge.zip)

## Résolution

Méthode : **git log**.

Le zip contient un depot git (`drop-in/`). Le flag n'est PAS dans les fichiers du HEAD mais dans le **message de commit** : `git log --all -p` le révèle. Reflexe : sur un depot, toujours `git log --all`, pas seulement `git log`.

## Flag

```
academy{t1m3m@ch1n3_b260a551}
```
