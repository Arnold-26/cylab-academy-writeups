# PW Crack 4

**Catégorie** : Général Skills · **Challenge** : #248 · **Résolu le** : 2026-11-23

## Énoncé

> Can you crack the password to get the flag?
> Download the password checker [here](https://challenge-files.cylabacademy.net/library/b1fecac0629eeb07add3a4371c6449060a0abbbbd461b98cd2b383f66d32fbb0/level4.py) and you'll
> need the encrypted [flag](https://challenge-files.cylabacademy.net/library/b1fecac0629eeb07add3a4371c6449060a0abbbbd461b98cd2b383f66d32fbb0/level4.flag.txt.enc) and the
> [hash](https://challenge-files.cylabacademy.net/library/b1fecac0629eeb07add3a4371c6449060a0abbbbd461b98cd2b383f66d32fbb0/level4.hash.bin) in the same directory too.
>
> There are 100 potential passwords with only 1 being correct. You can find these
> by examining the password checker script.

## Résolution

Méthode : **crack MD5 + XOR**.

Le script compare `md5(password)` à `level4.hash.bin`. En testant les candidats on trouve `ea43`, puis on déchiffre le `.enc` par XOR avec ce mot de passe (clé répétée).

## Flag

```
academy{fl45h_5pr1ng1ng_81dd449f}
```
