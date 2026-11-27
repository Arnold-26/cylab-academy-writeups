# bloat.py

**Catégorie** : Reverse Engineering · **Challenge** : #256 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **obfuscation par indices**.

Le script est obfusque : chaque caractere est `a[indice]` dans un alphabet de 95 caracteres. Le mot de passe compare est `happychance`. On l'envoie au programme, qui XOR `flag.txt.enc` avec ce mot de passe.

## Flag

```
academy{d30bfu5c4710n_f7w_468389f0}
```

## Ce qu'il faut retenir

—
