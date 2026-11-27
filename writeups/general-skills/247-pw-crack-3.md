# PW Crack 3

**Catégorie** : Général Skills · **Challenge** : #247 · **Résolu le** : 2026-11-23

## Énoncé

> Can you crack the password to get the flag?
> Download the password checker [here](https://challenge-files.cylabacademy.net/library/2b741086a592ccabd501acc798dfc974c0193e71c166b3addef3f87a6e572943/level3.py) and you'll
> need the encrypted [flag](https://challenge-files.cylabacademy.net/library/2b741086a592ccabd501acc798dfc974c0193e71c166b3addef3f87a6e572943/level3.flag.txt.enc) and the
> [hash](https://challenge-files.cylabacademy.net/library/2b741086a592ccabd501acc798dfc974c0193e71c166b3addef3f87a6e572943/level3.hash.bin) in the same directory too.
>
> There are 7 potential passwords with 1 being correct. You can find these by
> examining the password checker script.

## Résolution

Méthode : **crack MD5 + XOR**.

Le script compare `md5(password)` à `level3.hash.bin`. En testant les candidats on trouve `a9de`, puis on déchiffre le `.enc` par XOR avec ce mot de passe (clé répétée).

## Flag

```
academy{m45h_fl1ng1ng_de530414}
```
