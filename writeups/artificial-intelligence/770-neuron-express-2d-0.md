# 770 — Neuron Express 2D-0

**Événement** : picoCTF — AI Foundations I · **Catégorie** : Artificial Intelligence · **Auteur** : LT « syreal » Jones

## Énoncé

« Sondez un perceptron 2D à travers le réseau. Envoyez-lui des paires d'entiers (x, y) et observez
si le neurone s'active ou non. Utilisez ces réponses pour retrouver les poids et le biais entiers
sous-jacents, puis soumettez votre estimation avec la commande TEST pour gagner le flag. »

Connexion : `nc aureolin-pixie.cylabacademy.net <port>`. Les bornes d'entrée sont affichées à
l'ouverture de la session pour garder la recherche petite. Niveau *Easy*.

## Analyse

Le serveur implémente un perceptron à deux entrées :

```
sortie = 1  si  w1*x + w2*y + b >= 0   (le neurone « fires »)
sortie = 0  sinon                       (le neurone « stays quiet »)
```

Le dialogue affiche un compteur de requêtes `[n/128] (x,y)>` : le budget est de **128 sondes**. Le
triplet `(w1, w2, b)` est entier, ce qui borne l'espace des solutions et rend la recherche exacte.

Géométriquement, l'équation `w1*x + w2*y + b = 0` est une **droite** du plan. Le neurone sépare le
plan en deux demi-plans : la sortie 1 d'un côté, 0 de l'autre. Il n'y a donc pas de modèle à
apprendre, seulement une frontière à localiser. Trois paramètres, trois informations suffisent :
deux points de la droite (ou un point et une pente) donnent le triplet à un facteur d'échelle près.

Le protocole de la commande `TEST` confirme cette lecture : `TEST w1 w2 b` est validé sur **tous**
les entiers de la plage affichée, pas sur un échantillon. Autrement dit, le serveur vérifie que
l'hypothèse est cohérente partout, ce qui permet de soumettre une forme normalisée.

## Solution

On commence par les quatre coins du domaine affiché, pour déterminer l'orientation de la frontière.

```
[1/128] (x,y)> 0,0        → 0     (reste silencieux)
[2/128] (x,y)> 10,10      → 1
[3/128] (x,y)> 10,-10     → 1
[4/128] (x,y)> -10,10     → 0
[5/128] (x,y)> -10,-10    → 0
```

Tout le demi-plan `x > 0` déclenche, tout le demi-plan `x < 0` reste muet, et la valeur de `y` ne
change rien : la frontière est **verticale**, donc `w2 = 0`. Le signe indique par ailleurs que `w1`
est positif.

On cherche ensuite le seuil exact sur l'axe des x, à deux ordonnées différentes pour confirmer
l'indépendance en y :

```
[6/128]  0,10  → 0        [10/128]  0,-10 → 0
[7/128]  1,10  → 0        [11/128]  1,-10 → 0
[8/128]  2,10  → 0        [12/128]  2,-10 → 0
[9/128]  3,10  → 1        [13/128]  3,-10 → 1
```

Le basculement a lieu en `x = 3` **quelle que soit la valeur de y**. On a donc `w1*3 + b = 0` avec
des coefficients entiers : en normalisant par le pgcd, `w1 = 1` et `b = -3`. Le triplet primitif est
`(1, 0, -3)`.

Soumission :

```
[14/128] (x,y)> TEST 1 0 -3
Perfect match! Here is your flag:
academy{n3ur0n_expr_2d_0159e40e}
```

Le budget est très large pour cette méthode : quatorze requêtes sur cent vingt-huit. Le reste
pourrait servir à lever un doute, par exemple en vérifiant un point proche du seuil (`x = 3, y = 0`
doit déclencher) avant de soumettre.

## Pièges

- **Confondre pente et biais.** Un test symétrique `(10,10)` / `(-10,-10)` seul ne distingue pas une
  frontière verticale d'une frontière en diagonale : ce sont les quatre coins qui tranchent, parce
  qu'ils séparent les deux axes.
- **Chercher le seuil sur une seule ligne.** Tester `x` uniquement à `y = 10` laisse planer le doute
  sur `w2`. On refait la recherche à `y = -10` et on compare les basculements.
- **Oublier de normaliser.** `w1*3 + b = 0` admet `(1, 0, -3)`, mais aussi `(2, 0, -6)` ou
  `(-1, 0, 3)`. On soumet la forme primitive, positive en `w1`, puisque c'est la forme attendue par
  le serveur.
- **Format de `TEST`.** Trois entiers séparés par des espaces, sur la même ligne que l'invite,
  sans parenthèses ni virgules.
- **Épuiser le budget.** Le compteur est strict : on note les réponses au fur et à mesure, une
  session perdue ne se reprend pas.

**Pourquoi ça marche.** Un perceptron linéaire n'a pas de mémoire : sa sortie ne dépend que du signe
d'une forme linéaire. Sonder le signe en des points choisis revient à échantillonner la frontière
d'une droite ; trois points non alignés suffisent à la déterminer exactement, et les entiers rendent
la solution unique après normalisation. La « boîte noire » ne cache ici qu'une inéquation linéaire.

## Flag

```
academy{n3ur0n_expr_2d_0159e40e}
```
