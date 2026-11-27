# PW Crack 1

**Catégorie** : Général Skills · **Difficulté** : Easy · **Épreuve** : picoCTF 2022

## Énoncé

> Can you crack the password to get the flag?
> Download the password checker [here](https://challenge-files.cylabacademy.net/library/8bd8366ce732391ec41228eae748ee97bdcbba4e83438e196e6d8b4ecda2c224/level1.py) and you'll
> need the encrypted [flag](https://challenge-files.cylabacademy.net/library/8bd8366ce732391ec41228eae748ee97bdcbba4e83438e196e6d8b4ecda2c224/level1.flag.txt.enc) in the same
> directory too.

**Challenge** : #245

## Résolution

Lecture de `level1.py` : le mot de passe `8713` est en clair dans le test. Exécution avec ce mot de passe.

## Flag

```
academy{545h_r1ng1ng_d218163c}
```

## Ce qu'il faut retenir

Le vérificateur contient le secret : lire le source avant de brute-forcer.
