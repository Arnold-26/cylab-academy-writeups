# 240 — fixme1.py

**Événement** : Beginner picoMini 2022 · **Catégorie** : General Skills · **Auteur** : LT 'SYREAL' Jones

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

Un script `fixme1.py` est fourni avec la consigne « Fix the syntax error in this Python script to
print the flag ». Les indices précisent que l'indentation est significative en Python, rappellent
`nano` pour éditer depuis le webshell et indiquent que la fonction `str_xor` n'a pas besoin d'être
inversée.

## Analyse

L'exécution échoue avec une erreur d'indentation :

```
  File "fixme1.py", line 20
    print('That is correct! Here\'s your flag: ' + flag)
IndentationError: unexpected indent
```

En Python, l'indentation délimite les blocs : une ligne indentée sans bloc parent est une erreur de
syntaxe. Autour de la ligne 20, le script définit `flag_enc` puis calcule `flag`, et la ligne
`print` se retrouve décalée de deux espaces alors qu'elle devrait être au même niveau que
l'affectation précédente.

La logique du challenge est volontairement triviale : le flag est déjà calculé par le script
(`flag = str_xor(flag_enc, 'enkidu')`), seule la mise en forme du code empêche l'affichage. Il
n'est pas nécessaire de comprendre `str_xor` ni de retrouver la clé.

## Solution

1. Exécuter le script pour lire le message d'erreur :

```bash
python3 fixme1.py
```

2. Ouvrir le fichier à l'endroit indiqué (`nano fixme1.py` ou un éditeur quelconque) et examiner
   les lignes 18 à 21 :

```python
flag = str_xor(flag_enc, 'enkidu')
  print('That is correct! Here\'s your flag: ' + flag)
```

3. Supprimer les espaces en début de ligne `print` pour l'aligner sur l'affectation :

```python
flag = str_xor(flag_enc, 'enkidu')
print('That is correct! Here\'s your flag: ' + flag)
```

4. Relancer le script : il affiche le flag.

```bash
python3 fixme1.py
# That is correct! Here's your flag: picoCTF{...}
```

## Flag

`picoCTF{1nd3nt1ty_cr1515_09ee727a}`

## Sources

- https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/master/Beginner_picoMini_2022/General_Skills/fixme1.py.md — énoncé, indices, message d'erreur exact et extrait de code fautif
- https://qiita.com/colza_/items/99635806ea9fe7fc62fc — writeup court avec la valeur complète du flag
