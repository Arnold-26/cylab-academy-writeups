# Log Hunt

**Catégorie** : Général Skills · **Challenge** : #527 · **Résolu le** : 2026-11-23

## Énoncé

> Our server seems to be leaking pieces of a secret flag in its logs. The parts are scattered and sometimes repeated. Can you reconstruct the original flag?
> Download the [logs](https://challenge-files.cylabacademy.net/library/fefc39d7d9da79e3c3f78f0d7f12f520ca703a48a89fa1cac6856a5c2127a4e9/server.log) and figure out the full flag from the fragments.

## Résolution

Méthode : **fragments de log**.

Le fichier `server.log` contient 27 lignes `FLAGPART:` mais seulement **4 fragments distincts** (les autres sont des repetitions). Il faut les dedupliquer puis les concaténer dans l'ordre d'apparition pour reconstituer le flag.

## Flag

```
academy{us3_y0urlinux_sk1lls_cedfa5fb}
```
