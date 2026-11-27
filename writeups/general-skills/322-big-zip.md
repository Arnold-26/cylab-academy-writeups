# Big Zip

**Catégorie** : Général Skills · **Challenge** : #322 · **Résolu le** : 2026-11-23

## Énoncé

> Unzip this archive and find the flag.
> - [Download zip file](https://challenge-files.cylabacademy.net/library/b150f6f4d21f46fc2bba57ef49c7305541fa8e9bfa4241dfe8d066b99de56200/big-zip-files.zip)

## Résolution

Méthode : **grep recursif dans une archive**.

L'archive contient 8 732 fichiers `.txt` repartis dans des dossiers aux noms aléatoires. Le flag n'est pas dans un fichier au nom parlant : `grep -rilaE 'flag|academy' .` sur l'arborescence extraite le trouve dans un fichier quelconque. Chercher par CONTENU, pas par nom.

## Flag

```
academy{gr3p_15_m4g1c_ef8790dc}
```
