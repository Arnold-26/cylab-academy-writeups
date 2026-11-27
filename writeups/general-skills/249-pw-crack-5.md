# PW Crack 5

**Catégorie** : Général Skills · **Challenge** : #249 · **Résolu le** : 2026-11-23

## Énoncé

> Can you crack the password to get the flag?
> Download the password checker [here](https://challenge-files.cylabacademy.net/library/ab8c1cf7e7d8fda84ad80d01a77290b4ea24c6998837de149a179b1216941290/level5.py) and you'll
> need the encrypted [flag](https://challenge-files.cylabacademy.net/library/ab8c1cf7e7d8fda84ad80d01a77290b4ea24c6998837de149a179b1216941290/level5.flag.txt.enc) and the
> [hash](https://challenge-files.cylabacademy.net/library/ab8c1cf7e7d8fda84ad80d01a77290b4ea24c6998837de149a179b1216941290/level5.hash.bin) in the same directory too. Here's a
> [dictionary](https://challenge-files.cylabacademy.net/library/ab8c1cf7e7d8fda84ad80d01a77290b4ea24c6998837de149a179b1216941290/dictionary.txt) with all possible passwords based
> on the password conventions we've seen so far.

## Résolution

Méthode : **crack MD5 + XOR**.

Le script compare `md5(password)` à `level5.hash.bin`. En testant les candidats on trouve `7e5f`, puis on déchiffre le `.enc` par XOR avec ce mot de passe (clé répétée).

## Flag

```
academy{h45h_sl1ng1ng_e062d0ff}
```
