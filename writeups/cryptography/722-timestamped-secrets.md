# Timestamped Secrets

**Catégorie** : Cryptography · **Challenge** : #722 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **bruteforce du timestamp**.

La cle AES est `sha256(str(int(time.time())))[:16]` et l'enonce donne un timestamp approximatif. En balayant les timestamps autour de la valeur indiquee, celui qui donne un clair commencant par `academy{` est le bon (ici delta = 0).

## Flag

```
academy{sa3S_sEc9t_99162e4b}
```

## Ce qu'il faut retenir

—
