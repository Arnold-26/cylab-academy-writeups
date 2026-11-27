# Blame Game

**Catégorie** : General Skills · **Challenge** : #405 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **git log -p (historique complet)**.

Le depot a des dizaines de commits 'important business work'. Le flag n'est pas dans le fichier courant mais dans l'**historique** : `git log --all -p | grep academy`. Piege : le zip s'extrait dans `drop-in/`.

## Flag

```
academy{@sk_th3_1nt3rn_43769efb}
```

## Ce qu'il faut retenir

—
