# Specialer

**Catégorie** : General Skills · **Challenge** : #378 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **shell sans commandes : globbing + $(<file)**.

Le shell n'a ni `ls` ni `cat` (chroot minimal : /bin/bash seulement). On liste avec le **globbing** (`echo *`, `echo abra/*`) et on lit avec la substitution de fichier `echo $(<ala/kazam.txt)`.

## Flag

```
academy{y0u_d0n7_4ppr3c1473_wh47_w3r3_d01ng_h3r3_f7316569}
```

## Ce qu'il faut retenir

—
