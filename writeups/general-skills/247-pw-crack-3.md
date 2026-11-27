# PW Crack 3

**Catégorie** : General Skills · **Challenge** : #247 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **crack MD5 + XOR**.

Le script compare `md5(password)` a `level3.hash.bin`. En testant les candidats on trouve `a9de`, puis on dechiffre le `.enc` par XOR avec ce mot de passe (cle repetee).

## Flag

```
academy{m45h_fl1ng1ng_de530414}
```

## Ce qu'il faut retenir

—
