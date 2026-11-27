# Python Wrangling

**Catégorie** : General Skills · **Challenge** : #166 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **execution de script + mot de passe**.

`ende.py` prend `-d <fichier>` puis lit le mot de passe sur **stdin**. `echo $(cat password.txt) | python3 ende.py -d flag.txt.en`. Piege : passer le fichier en premier argument sans `-d` -> `Unrecognized first argument`.

## Flag

```
academy{4p0110_1n_7h3_h0us3_d6af8f37}
```

## Ce qu'il faut retenir

—
