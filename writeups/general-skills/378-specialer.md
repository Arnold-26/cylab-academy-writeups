# Specialer

**Catégorie** : Général Skills · **Challenge** : #378 · **Résolu le** : 2026-11-23

## Énoncé

> Reception of Special has been cool to say the least. That's why we made an
> exclusive version of Special, called Secure Comprehensive Interface for
> Affecting Linux Empirically Rad, or just 'Specialer'. With Specialer, we really
> tried to remove the distractions from using a shell. Yes, we took out spell
> checker because of everybody's complaining. But we think you will be excited
> about our new, reduced feature set for keeping you focused on what needs it the
> most. Please start an instance to test your very own copy of Specialer.

## Résolution

Méthode : **shell sans commandes : globbing + $(<file)**.

Le shell n'a ni `ls` ni `cat` (chroot minimal : /bin/bash seulement). On liste avec le **globbing** (`echo *`, `echo abra/*`) et on lit avec la substitution de fichier `echo $(<ala/kazam.txt)`.

## Flag

```
academy{y0u_d0n7_4ppr3c1473_wh47_w3r3_d01ng_h3r3_f7316569}
```
