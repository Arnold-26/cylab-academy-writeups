# timer

**Catégorie** : Reverse Engineering · **Challenge** : #381 · **Résolu le** : 2026-11-23

## Énoncé

> You will find the flag after analysing this apk
> Download [here](https://challenge-files.cylabacademy.net/library/b31248aec6287cbe220d0dbfa55e216b87e6175b3561d441062bfdd018f3cacc/timer.apk).

## Résolution

Méthode : **unzip APK + grep dex**.

L'APK contient plusieurs `classes*.dex`. Un simple `grep -a 'academy{'` sur le contenu decompresse trouve le flag en clair dans `classes3.dex`.

## Flag

```
academy{t1m3r_r3v3rs3d_succ355fully_17496}
```
