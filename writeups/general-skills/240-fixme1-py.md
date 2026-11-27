# 240 — fixme1.py

**Événement** : Beginner picoMini 2022 · **Catégorie** : General Skills

## Énoncé

Un script `fixme1.py` est fourni avec la consigne « Fix the syntax error in this Python script to print the flag ». Les indices précisent que l'indentation est significative en Python, rappellent `nano` pour éditer depuis le webshell et indiquent que la fonction `str_xor` n'a pas besoin d'être inversée.

## Analyse

L'exécution échoue avant tout calcul :

```
  File "fixme1.py", line 20
    print('That is correct! ...' + flag)
IndentationError: unexpected indent
```

En Python, l'indentation délimite les blocs : une ligne décalée sans bloc parent est une erreur de syntaxe. Autour de la ligne 20, le script définit `flag_enc` puis calcule `flag`, et la ligne `print` se retrouve décalée de deux espaces alors qu'elle devrait être au même niveau que l'affectation précédente.

La logique du challenge est volontairement triviale : le flag est déjà calculé par le script (`flag = str_xor(flag_enc, 'enkidu')`), seule la mise en forme empêche l'affichage. Il n'est pas nécessaire de comprendre `str_xor` ni de retrouver la clé, le script la contient.

Le troisième indice coupe d'ailleurs la piste la plus tentante : réimplémenter le déchiffrement. Le décodage a déjà lieu à l'exécution, on ne fait que réparer la syntaxe pour laisser le programme aller au bout.

## Solution

### 1. Reproduire l'erreur

```bash
python3 fixme1.py
```

Le message donne le numéro de ligne exact, ce qui évite de relire tout le script à l'œil.

### 2. Ouvrir le fichier à l'endroit indiqué

Depuis le webshell, `nano` est disponible :

```bash
nano fixme1.py
```

Les lignes 18 à 21 ressemblent à ceci :

```python
flag = str_xor(flag_enc, 'enkidu')
  print('That is correct! ...' + flag)
```

### 3. Réaligner la ligne fautive

On supprime les deux espaces en tête de la ligne `print` pour l'aligner sur l'affectation :

```python
flag = str_xor(flag_enc, 'enkidu')
print('That is correct! ...' + flag)
```

On sauvegarde avec `Ctrl+O`, `Entrée`, puis `Ctrl+X` : sur un webshell, quitter sans écrire est l'erreur classique.

### 4. Relancer

```bash
python3 fixme1.py
# That is correct! Here's your flag: <flag>
```

Le script affiche le flag tel qu'il le calcule ; aucun autre travail n'est nécessaire.

### Pourquoi ça marche

Le script calcule déjà le flag ; l'interpréteur s'arrête avant parce que la ligne `print` est décalée. Une fois l'indentation corrigée, l'exécution va jusqu'au bout et affiche la valeur.

## Pièges

- **Casser le XOR** : les indices disent explicitement de ne pas inverser `str_xor` ; le script calcule déjà le flag.
- **Mélanger tabulations et espaces** : Python 3 refuse l'incohérence (`TabError`) ; on reprend le style d'indentation du fichier.
- **Corriger une autre ligne** : l'interpréteur pointe la ligne 20, mais une ligne voisine peut aussi être mal alignée.
- **Éditer sans sauvegarder** : dans `nano` sur un webshell, on quitte souvent avec `Ctrl+X` sans confirmer l'écriture.
- **Recopier le script à la main** : l'apostrophe échappée du message se perd facilement et provoque une nouvelle erreur de syntaxe.

## Flag

Flag validé sur la plateforme (valeur non conservée).
