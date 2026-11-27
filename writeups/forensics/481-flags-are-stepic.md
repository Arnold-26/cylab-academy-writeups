# flags are stepic

**Catégorie** : Forensics · **Challenge** : #481 · **Résolu le** : 2026-11-24

## Énoncé

> A group of underground hackers might be using this legit site to communicate. Use your forensic techniques to uncover their message

## Résolution

Méthode : **steganographie avec l'outil stepic**.

Le site liste 246 drapeaux de pays. L'un d'eux (`upz.png`) contient un message cache avec l'outil **stepic** (steganographie dans les pixels, pas de simple LSB). `stepic.decode()` révèle le flag.

## Flag

```
academy{fl4g_h45_fl4ga947c25f}
```

## Scripts

- [`solve.py`](../../solve/481/solve.py)
- *6 variantes intermediaires dans `solve/481/archive/`*
