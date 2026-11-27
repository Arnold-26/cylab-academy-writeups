# Commitment Issues

**Catégorie** : General Skills · **Challenge** : #411 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **git log -p (fichier supprime)**.

Le depot contient deux commits : `create flag` puis `remove sensitive info`. Le second supprime le fichier, mais `git log --all -p` rejoue le diff et le flag reste dans l'historique. Piege : le zip s'extrait dans un sous-dossier `drop-in/` — lancer git dans le bon repertoire.

## Flag

```
academy{s@n1t1z3_f1ce74e2}
```

## Ce qu'il faut retenir

—
