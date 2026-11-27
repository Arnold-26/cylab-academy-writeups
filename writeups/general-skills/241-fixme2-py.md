# 241 — fixme2.py

**Événement** : Beginner picoMini 2022 · **Catégorie** : General Skills · **Auteur** : LT 'SYREAL' Jones

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

Un second script `fixme2.py` est fourni, toujours avec la consigne « Fix the syntax error in this
Python script to print the flag ». L'indice décisif demande si l'égalité et l'affectation utilisent
le même symbole.

## Analyse

L'exécution échoue sur une syntaxe invalide :

```
  File "fixme2.py", line 22
    if flag = "":
       ^^^^^^^^^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

Python distingue deux opérateurs :

- `=` est l'affectation (elle renvoie `None` en tant qu'expression) ;
- `==` est la comparaison d'égalité.

Une affectation dans la condition d'un `if` n'est pas une expression valide en Python, contrairement
à d'autres langages où `if (x = y)` compile et provoque des bugs silencieux. Le message d'erreur
suggère d'ailleurs explicitement `==`. Le script calcule déjà le flag via `str_xor`, comme dans
`fixme1.py` : la correction est purement syntaxique.

## Solution

1. Reproduire l'erreur :

```bash
python3 fixme2.py
```

2. Corriger la ligne 22 dans un éditeur (`nano fixme2.py`) :

```python
if flag = "":
```

devient

```python
if flag == "":
```

3. Relancer :

```bash
python3 fixme2.py
# That is correct! Here's your flag: picoCTF{...}
```

4. En cas de doute sur la ligne à modifier, `grep -n "if flag" fixme2.py` isole directement la
   condition fautive.

## Flag

`picoCTF{3qu4l1ty_n0t_4551gnm3nt_e8814d03}`

## Sources

- https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/master/Beginner_picoMini_2022/General_Skills/fixme2.py.md — énoncé, indices, message d'erreur complet et correction `=` → `==`
- https://xavierj.me/picoctf/fixme1--2.py/ — writeup couvrant les deux scripts, avec la valeur complète des deux flags
