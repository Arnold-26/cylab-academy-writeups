# MacroHard WeakEdge

**Catégorie** : Forensics · **Challenge** : #130 · **Résolu le** : 2026-11-23

## Énoncé

> I've hidden a flag in this file. Can you find it?
> [Forensics_is_fun.pptm](https://challenge-files.cylabacademy.net/library/ef35dfe613527d28fe872d94179b53bc1a0497ddecf57e51d160c910be3a8e8a/Forensics_is_fun.pptm)

## Résolution

Méthode : **fichier cache dans l'archive OOXML**.

Un `.pptm` est une archive ZIP. Le VBA (`ppt/vbaProject.bin`) contient un **leurre** (`not_flag` -> "sorry_but_this_isn't_it"). Le vrai flag est dans un fichier **non référence** par `[Content_Types].xml` : `ppt/slideMasters/hidden`, qui contient du base64 **avec des espaces** — il faut les retirer avant de decoder.

## Flag

```
academy{D1d_u_kn0w_ppts_r_z1p5}
```
