# PW Crack 4

**Catégorie** : General Skills · **Challenge** : #248 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **crack MD5 + XOR**.

Le script compare `md5(password)` a `level4.hash.bin`. En testant les candidats on trouve `ea43`, puis on dechiffre le `.enc` par XOR avec ce mot de passe (cle repetee).

## Flag

```
academy{fl45h_5pr1ng1ng_81dd449f}
```

## Ce qu'il faut retenir

—
