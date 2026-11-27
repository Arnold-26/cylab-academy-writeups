# keygenme-py

**Catégorie** : Reverse Engineering · **Challenge** : #121 · **Résolu le** : 2026-11-23

## Énoncé

> [keygenme-trial.py](https://challenge-files.cylabacademy.net/library/f4454c2722efb6225e1ebabff8e0d802c592aef27e436433863773badc76a1f7/keygenme-trial.py)

## Résolution

Méthode : **sha256 tronque**.

Le flag est `academy{1n_7h3_kk3y_of_` + 8 caractères + `}`. `check_key` compare chaque caractère dynamique à `sha256("MILLER").hexdigest()[i]` avec les indices 4,5,3,6,2,7,1,8 dans cet ordre. On recalcule le hash et on assemble.

## Flag

```
academy{1n_7h3_kk3y_of_9edf443b}
```
