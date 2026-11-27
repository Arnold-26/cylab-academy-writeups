# bloat.py

**Catégorie** : Reverse Engineering · **Challenge** : #256 · **Résolu le** : 2026-11-23

## Énoncé

> Can you get the flag?
> Run this [Python program](https://challenge-files.cylabacademy.net/library/ec210162639a40cca7b4d644dccdc74d1917ae7395bb122e28e02bf01e957279/bloat.flag.py) in the same directory
> as this [encrypted flag](https://challenge-files.cylabacademy.net/library/ec210162639a40cca7b4d644dccdc74d1917ae7395bb122e28e02bf01e957279/flag.txt.enc).

## Résolution

Méthode : **obfuscation par indices**.

Le script est obfusque : chaque caractère est `a[indice]` dans un alphabet de 95 caractères. Le mot de passe compare est `happychance`. On l'envoie au programme, qui XOR `flag.txt.enc` avec ce mot de passe.

## Flag

```
academy{d30bfu5c4710n_f7w_468389f0}
```
