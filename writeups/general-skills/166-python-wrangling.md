# Python Wrangling

**Catégorie** : Général Skills · **Challenge** : #166 · **Résolu le** : 2026-11-23

## Énoncé

> Python scripts are invoked kind of like programs in the Terminal...
> Can you run [ende.py](https://challenge-files.cylabacademy.net/library/9524fad56d411feaebef2bff00dedd811236de9859d90c446ac88ffac47e0192/ende.py) using [password.txt](https://challenge-files.cylabacademy.net/library/9524fad56d411feaebef2bff00dedd811236de9859d90c446ac88ffac47e0192/password.txt) to get [flag.txt.en](https://challenge-files.cylabacademy.net/library/9524fad56d411feaebef2bff00dedd811236de9859d90c446ac88ffac47e0192/flag.txt.en)?

## Résolution

Méthode : **exécution de script + mot de passe**.

`ende.py` prend `-d <fichier>` puis lit le mot de passe sur **stdin**. `echo $(cat password.txt) | python3 ende.py -d flag.txt.en`. Piege : passer le fichier en premier argument sans `-d` -> `Unrecognized first argument`.

## Flag

```
academy{4p0110_1n_7h3_h0us3_d6af8f37}
```
