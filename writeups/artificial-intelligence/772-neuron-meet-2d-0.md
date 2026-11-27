# 772 — Neuron Meet 2D-0

**Événement** : picoCTF — AI Foundations I · **Catégorie** : Artificial Intelligence · **Auteur** : LT « syreal » Jones

## Énoncé

« Sondez un perceptron 2D à travers le réseau. Envoyez-lui des paires de nombres (x, y) et observez
si le neurone s'active. Utilisez ces réponses pour retrouver la frontière de décision, puis alignez
les **huit dernières sorties** sur l'ASCII de `p` (01110000) pour gagner le flag. »

Connexion : `nc aureolin-pixie.cylabacademy.net <port>`, bornes d'entrée affichées à la connexion.
**Contrainte supplémentaire** : on ne peut pas soumettre deux fois de suite la même paire `(x, y)`.
Niveau *Easy*.

## Analyse

Même modèle que les autres challenges de la série :

```
sortie = 1 si w1*x + w2*y + b >= 0
sortie = 0 sinon
```

L'objectif, en revanche, n'est pas de deviner les poids : il n'y a pas de commande `TEST` ici. Il
faut produire une **séquence de 8 bits** égale à `01110000`, soit `0x70`, le code ASCII de `p`. Le
serveur affiche en continu :

```
Recent outputs (n/8): ........
```

Seuls les huit derniers tirages comptent, et la fenêtre est glissante. Le problème se reformule
donc ainsi : choisir une suite de huit points dont la classe prédite soit exactement `0 1 1 1 0 0 0 0`.

Deux stratégies sont possibles.

**Boîte noire.** On connaît la sortie désirée pour huit points ; il suffit de trouver, pour chaque
bit, un point dont on sait qu'il produit cette valeur. Les extrêmes du domaine affiché sont des
candidats naturels : ils sont loin de la frontière, donc leur classe est stable.

**Boîte blanche.** On localise d'abord la frontière comme dans `Neuron Express 2D-0` (quatre coins,
puis recherche du seuil), puis on choisit les points de part et d'autre pour forcer chaque bit.

La méthode employée est la première : elle coûte zéro sonde préparatoire et ne dépend pas de la
position exacte de la droite. Les quatre points cardinaux extrêmes suffisent.

## Solution

Séquence gagnante, telle qu'observée sur l'instance :

```
0,0     → 0    Recent outputs (1/8): 0
10,10   → 1    Recent outputs (2/8): 01
0,10    → 1    Recent outputs (3/8): 011
10,0    → 1    Recent outputs (4/8): 0111
-10,-10 → 0    Recent outputs (5/8): 01110
-10,10  → 0    Recent outputs (6/8): 011100
10,-10  → 0    Recent outputs (7/8): 0111000
-10,0   → 0    Recent outputs (8/8): 01110000
```

Le serveur valide alors le motif :

```
Pattern matched! ASCII 'p' unlocked. Here is your flag:
academy{2d_n3ur0n_m3t_dadc9561}
```

Le point délicat est l'ordre : les bits sont consommés dans l'ordre d'arrivée, donc la séquence doit
être préparée **avant** de se connecter. Une fois les huit bons points envoyés d'affilée, le motif
est complet.

Si l'on veut vérifier la logique sans consommer la fenêtre, on peut sonder d'abord quelques points
hors séquence, puis recommencer une session : la fenêtre repart de zéro à chaque connexion.

## Pièges

- **Deux fois la même paire d'affilée.** Le serveur refuse la répétition immédiate : marteler un
  point qui renvoie 0 ou 1 ne fonctionne pas. Il faut varier légèrement les entrées tout en restant
  du même côté de la frontière, par exemple `10,0` puis `10,-10`.
- **Fenêtre glissante.** Les huit tirages doivent être **consécutifs**. Un test raté décale la
  fenêtre et le motif est perdu : il faut alors rejouer huit points corrects, pas un seul.
- **Ordre des points.** `0,0` puis `10,10` ne donne pas le même motif que `10,10` puis `0,0`. La
  séquence est écrite à l'avance, pas improvisée.
- **Bornes du domaine.** Les coordonnées hors des bornes affichées sont rejetées ou ramenées à la
  frontière, ce qui fausse le bit. On reste dans la plage annoncée à la connexion.
- **Format de saisie.** `x,y` sans espace, avec une virgule : le parseur du service est strict.

**Pourquoi ça marche.** La sortie d'un perceptron est une fonction déterministe de l'entrée. En
choisissant huit points dont la classe est connue à l'avance (extrêmes du domaine), on écrit le mot
binaire souhaité sans jamais connaître les poids : le réseau sert de générateur de bits, et c'est
l'ordre d'arrivée qui porte l'information. Le challenge illustre qu'une interface de prédiction
expose un canal d'écriture, pas seulement un oracle.

## Flag

```
academy{2d_n3ur0n_m3t_dadc9561}
```
