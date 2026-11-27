# Related Messages

**Catégorie** : Cryptography · **Challenge** : #713 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **Franklin-Reiter**.

Deux chiffres RSA du meme message avec une faute de frappe (ecart de 3). L'attaque de **Franklin-Reiter** calcule le pgcd des polynomes `x^e - c1` et `(x+3)^e - c2` modulo n ; le pgcd est `x - m`.

## Flag

```
academy{m3ssage_w1th_typ0}
```

## Ce qu'il faut retenir

—
