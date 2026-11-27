# Special

**Catégorie** : General Skills · **Challenge** : #377 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **bypass du spell-checker par variables**.

Le shell (`/usr/local/Special.py`) capitalise le premier caractere de chaque mot et corrige l'orthographe, ce qui casse `ls`->`Ls`, `cat`->`Cat`. Il refuse aussi les chemins avec `/` en tete. Bypass : affecter une variable dont le nom est DEJA une majuscule : `A=ls;$A` puis `A=cat;$A blargh/*`. Le spell-checker change meme les arguments (`blargh` -> `large`), donc garder les globs.

## Flag

```
academy{5p311ch3ck_15_7h3_w0r57_9fd4af4a}
```
