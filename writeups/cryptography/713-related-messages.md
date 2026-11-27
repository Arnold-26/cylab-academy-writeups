# Related Messages

**Catégorie** : Cryptography · **Challenge** : #713 · **Résolu le** : 2026-11-23

## Énoncé

> Oops! I have a typo in my first message so i sent it again! I used RSA twice so this is secure right?
> [chall.py](https://challenge-files.cylabacademy.net/library/d33371f1a01fd9671ac08d9ce0a486325fd0e8ed66ce83fc97ee9a5a07a64cb9/chall.py)
> [output.txt](https://challenge-files.cylabacademy.net/library/d33371f1a01fd9671ac08d9ce0a486325fd0e8ed66ce83fc97ee9a5a07a64cb9/output.txt)

## Résolution

Méthode : **Franklin-Reiter**.

Deux chiffres RSA du même message avec une faute de frappe (écart de 3). L'attaque de **Franklin-Reiter** calcule le pgcd des polynomes `x^e - c1` et `(x+3)^e - c2` modulo n ; le pgcd est `x - m`.

## Flag

```
academy{m3ssage_w1th_typ0}
```
