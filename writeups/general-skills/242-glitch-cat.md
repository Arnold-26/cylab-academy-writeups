# Glitch Cat

**Catégorie** : General Skills · **Challenge** : #242 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **eval de l'expression Python**.

Le service renvoie `'academy{gl17ch_m3_n07_' + chr(0x63) + ... + '}'` : ce n'est pas le flag mais une **expression Python**. Il faut l'evaluer (avec `chr` disponible) pour obtenir le flag.

## Flag

```
academy{gl17ch_m3_n07_cbc18a24}
```
