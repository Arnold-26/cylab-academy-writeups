# 241 — fixme2.py

**Événement** : Beginner picoMini 2022 · **Catégorie** : Général Skills

## Énoncé

Un second script `fixme2.py` est fourni, toujours avec la consigne « Fix the syntax error in this Python script to print the flag ». L'indice décisif demande si l'égalité et l'affectation utilisent le même symbole.

## Analyse

L'exécution échoue sur une syntaxe invalide :

```
  File "fixme2.py", line 22
    if flag = "":
       ^^^^^^^^^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

Python distingue deux opérateurs :

- `=` est l'affectation ; en tant qu'expression elle ne renvoie pas de valeur utile, elle est réservée aux instructions ;
- `==` est la comparaison d'égalité et produit un booléen.

Une affectation dans la condition d'un `if` n'est donc pas une expression valide en Python, contrairement à d'autres langages où `if (x = y)` compile et provoque des bugs silencieux. Le message d'erreur propose d'ailleurs explicitement `==`, et mentionne `:=` (l'opérateur « walrus »), qui serait une autre façon — inutile ici — d'assigner dans une condition.

Comme dans `fixme1.py`, le script calcule déjà le flag via `str_xor` : la correction est purement syntaxique, il n'y a aucune valeur à recalculer. Le `if` corrigé teste simplement que la chaîne n'est pas vide avant de l'afficher, ce qui est vrai une fois le flag calculé.

## Solution

### 1. Reproduire l'erreur

```bash
python3 fixme2.py
```

### 2. Localiser la condition fautive

```bash
grep -n "if flag" fixme2.py
```

La commande isole directement la ligne 22 et évite de parcourir le script dans le webshell.

### 3. Corriger l'opérateur

```python
if flag = "":
```

devient

```python
if flag == "":
```

On garde le reste de la ligne intact : les guillemets vides et le deux-points final sont corrects.

### 4. Relancer

```bash
python3 fixme2.py
# That is correct! Here's your flag: <flag>
```

Le script affiche le flag ; on le colle sur la plateforme.

### Pourquoi ça marche

Le script calcule le flag avant le `if` ; seule la condition est mal écrite. Remplacer `=` par `==` rend la comparaison valide, la condition est vraie (chaîne non vide) et l'affichage a lieu.

## Pièges

- **Remplacer `=` par `:=`** : le walrus est accepté par Python 3.8+ mais change la sémantique (il affecte puis évalue), ce n'est pas ce que le script attend.
- **Corriger au hasard une autre affectation** : le fichier contient d'autres `=` légitimes ; seul le `if` est fautif.
- **Oublier le second `=`** : une correction partielle (`if flag = ""` → `if flag =""`) laisse la même erreur.
- **Confondre les deux challenges** : `fixme1.py` est une erreur d'indentation, `fixme2.py` une erreur d'opérateur ; les correctifs ne s'échangent pas.
- **Sauvegarde dans `nano`** : sans `Ctrl+O` confirmé, on relance l'ancienne version et l'erreur persiste.
