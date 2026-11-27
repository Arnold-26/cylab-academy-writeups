# convertme.py

**Catégorie** : Général Skills · **Difficulté** : Easy · **Épreuve** : picoCTF 2022

## Énoncé

> Run the Python script and convert the given number from decimal to binary to
> get the flag.
> [Download Python script](https://challenge-files.cylabacademy.net/library/d507213597114cdf0943d7f7c585eab624e16586a7cdcb88229fd24c143128a1/convertme.py)

**Challenge** : #239

## Résolution

Script exécuté en interactif : il demande la conversion d'un nombre aléatoire en binaire, réponse calculée avec `bin(n)[2:]`.

## Flag

```
academy{4ll_y0ur_b4535_fff0af3d}
```

## Ce qu'il faut retenir

Automatiser l'interactif : tubes binaires, sans quoi Windows traduit `\n` en `\r\n` et casse la saisie.
