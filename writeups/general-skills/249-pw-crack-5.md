# PW Crack 5

**Catégorie** : General Skills · **Challenge** : #249 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **crack MD5 + XOR**.

Le script compare `md5(password)` a `level5.hash.bin`. En testant les candidats on trouve `7e5f`, puis on dechiffre le `.enc` par XOR avec ce mot de passe (cle repetee).

## Flag

```
academy{h45h_sl1ng1ng_e062d0ff}
```

## Ce qu'il faut retenir

—
