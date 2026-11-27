# timer

**Catégorie** : Reverse Engineering · **Challenge** : #381 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **unzip APK + grep dex**.

L'APK contient plusieurs `classes*.dex`. Un simple `grep -a 'academy{'` sur le contenu decompresse trouve le flag en clair dans `classes3.dex`.

## Flag

```
academy{t1m3r_r3v3rs3d_succ355fully_17496}
```

## Ce qu'il faut retenir

—
