# Log Hunt

**Catégorie** : General Skills · **Challenge** : #527 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **fragments de log**.

Le fichier `server.log` contient 27 lignes `FLAGPART:` mais seulement **4 fragments distincts** (les autres sont des repetitions). Il faut les dedupliquer puis les concatener dans l'ordre d'apparition pour reconstituer le flag.

## Flag

```
academy{us3_y0urlinux_sk1lls_cedfa5fb}
```
