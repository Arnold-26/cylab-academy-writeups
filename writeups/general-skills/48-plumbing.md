# 48 — plumbing

**Événement** : picoCTF 2019 · **Catégorie** : General Skills · **Auteur** : Alex Fulton/Danny Tunitits

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

Un service réseau renvoie un flux continu de lignes sans intérêt (« Not a flag either », « I don't
think this is a flag either », etc.) parmi lesquelles se trouve une seule ligne au format
`picoCTF{...}`. L'indice parle de « pipe » et de la nécessité de garder la sortie du programme
hors d'un fichier.

## Analyse

Le programme écrit énormément de lignes, bien plus que ce qu'un terminal peut afficher : le flag
défile et disparaît du scrollback. Deux stratégies fonctionnelles :

- rediriger la sortie vers un fichier (`nc host port > out.txt`) puis chercher dedans, ce qui
  oblige à attendre la fermeture de la connexion ;
- brancher directement `stdout` de `nc` sur `stdin` de `grep` avec le tube `|`, pour ne laisser
  passer que la ligne utile dès qu'elle arrive.

La seconde est la réponse attendue : c'est la composition Unix de base — un programme fait une
chose, le tube assemble les programmes sans les modifier.

## Solution

1. Vérifier le comportement brut du service :

```bash
nc jupiter.challenges.picoctf.org 7480
```

2. Filtrer le flux en direct sur le motif du flag :

```bash
nc jupiter.challenges.picoctf.org 7480 | grep picoCTF
```

3. La commande affiche immédiatement la seule ligne correspondante, qui contient le flag.

4. Variantes équivalentes, utiles si le flux est très long :

```bash
nc jupiter.challenges.picoctf.org 7480 | grep -m1 "picoCTF{"
nc jupiter.challenges.picoctf.org 7480 > out.txt && grep picoCTF out.txt
```

## Flag

`picoCTF{digital_plumb3r_ea8bfec7}`

## Sources

- https://eszfrigyes.com/2023/02/ctf-writeup-plumbing-picoctf/ — énoncé, commande `nc ... | grep picoCTF` et flag complet affiché
- https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/master/picoCTF_2019/General_Skills/plumbing.md — énoncé, indices sur les pipes, extrait du flux renvoyé par le service
