# PW Crack 2

**Catégorie** : Général Skills · **Difficulté** : Easy · **Épreuve** : picoCTF 2022

## Énoncé

> Can you crack the password to get the flag?
> Download the password checker [here](https://challenge-files.cylabacademy.net/library/227623e9501e3a811cdf5b1c7a2079f75b2e9ab243364a38830e0a4a2943ce2e/level2.py) and you'll
> need the encrypted [flag](https://challenge-files.cylabacademy.net/library/227623e9501e3a811cdf5b1c7a2079f75b2e9ab243364a38830e0a4a2943ce2e/level2.flag.txt.enc) in the same directory
> too.

**Challenge** : #246

## Résolution

Le mot de passe est construit par concaténation : `chr(0x34)+chr(0x65)+chr(0x63)+chr(0x39)` = `4ec9`.

## Flag

```
academy{tr45h_51ng1ng_d99a9ef4}
```

## Ce qu'il faut retenir

Désobfusquer une expression `chr()` se fait en l'évaluant.
