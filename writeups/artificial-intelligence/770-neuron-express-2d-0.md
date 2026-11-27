# 770 — Neuron Express 2D-0

**Événement** : picoCTF — AI Foundations I · **Catégorie** : Artificial Intelligence · **Auteur** : LT « syreal » Jones

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

« Sondez un perceptron 2D à travers le réseau. Envoyez-lui des paires d'entiers (x, y) et
observez si le neurone s'active ou non. Utilisez ces réponses pour retrouver les poids et le
biais entiers sous-jacents, puis soumettez votre estimation avec la commande TEST pour gagner
le flag. »

Connexion : `nc aureolin-pixie.cylabacademy.net <port>`. Les bornes d'entrée sont affichées à
la connexion pour garder la recherche petite. Niveau *Easy*, tags *Artificial Intelligence, AI
Foundations I*.

## Analyse

Le serveur implémente un perceptron à deux entrées :

```
sortie = 1  si  w1*x + w2*y + b >= 0   (le neurone « fires »)
sortie = 0  sinon                       (le neurone « stays quiet »)
```

Le budget est de **128 requêtes** (`[n/128] (x,y)>`). Géométriquement, la frontière
`w1*x + w2*y + b = 0` est une **droite** du plan : il suffit de localiser la droite, pas
d'apprendre un modèle. Les poids et le biais sont des entiers, donc l'intersection avec les
axes donne directement `w1`, `w2`, `b` à un facteur d'échelle entier près.

## Solution

Méthode par balayage, en quatre points extrêmes puis en suivant l'axe :

```
[1/128] (x,y)> 0,0        → 0     (reste silencieux)
[2/128] (x,y)> 10,10      → 1
[3/128] (x,y)> 10,-10     → 1
[4/128] (x,y)> -10,10     → 0
[5/128] (x,y)> -10,-10    → 0
```

Tout le côté `x > 0` déclenche, tout le côté `x < 0` non : la frontière est verticale (`w2 = 0`).
On cherche ensuite le seuil exact sur x à deux ordonnées différentes :

```
[6/128]  0,10  → 0        [10/128]  0,-10 → 0
[7/128]  1,10  → 0        [11/128]  1,-10 → 0
[8/128]  2,10  → 0        [12/128]  2,-10 → 0
[9/128]  3,10  → 1        [13/128]  3,-10 → 1
```

Le basculement a lieu en `x = 3` **quelle que soit la valeur de y** : c'est bien une droite
verticale, donc `w2 = 0`, et `w1*3 + b = 0` avec des coefficients entiers premiers entre eux
⇒ `w1 = 1`, `b = -3`.

Soumission :

```
[14/128] (x,y)> TEST 1 0 -3
Perfect match! Here is your flag:
academy{n3ur0n_expr_2d_0159e40e}
```

Le serveur vérifie le triplet sur **tous** les entiers de la plage, ce qui explique que la
commande s'appelle `TEST` : c'est une validation exhaustive de l'hypothèse, pas un simple
échantillon.

## Flag

```
academy{n3ur0n_expr_2d_0159e40e}
```

## Sources

- https://shukularuni.neocities.org/guide/ctf/picoctf/ai/Neuron_Express_2D-0
- https://medium.com/@ramsarathi369/neuron-express-2d-0-ctf-writeup-finding-a-perceptrons-weights-and-bias-f7c9f2a90b82
- https://learn.cylabacademy.org/library/770
