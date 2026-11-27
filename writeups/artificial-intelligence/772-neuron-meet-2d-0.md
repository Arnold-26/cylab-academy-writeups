# 772 — Neuron Meet 2D-0

**Événement** : picoCTF — AI Foundations I · **Catégorie** : Artificial Intelligence · **Auteur** : LT « syreal » Jones

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

« Sondez un perceptron 2D à travers le réseau. Envoyez-lui des paires de nombres (x, y) et
observez si le neurone s'active. Utilisez ces réponses pour retrouver la frontière de décision,
puis alignez les **huit dernières sorties** sur l'ASCII de `p` (01110000) pour gagner le flag. »

Connexion : `nc aureolin-pixie.cylabacademy.net <port>`, bornes d'entrée affichées à la
connexion. **Contrainte supplémentaire** : on ne peut pas soumettre deux fois de suite la même
paire `(x, y)`. Niveau *Easy*, AI Foundations I.

## Analyse

Même modèle que les autres challenges de la série :

```
sortie = 1 si w1*x + w2*y + b >= 0, sinon 0
```

Mais l'objectif diffère : il ne faut pas *deviner les poids* (pas de commande `TEST` ici), il
faut produire une **séquence de 8 bits** égale à `01110000`, soit `0x70` = `p` en ASCII. Le
serveur affiche en continu `Recent outputs (n/8): ...` et seuls les huit derniers comptent.

Deux stratégies possibles :

1. **Boîte noire** — on connaît la sortie désirée pour huit points ; il suffit de choisir huit
   points dont on sait qu'ils déclenchent ou non, par exemple en sondant d'abord les extrêmes
   du domaine affiché.
2. **Boîte blanche** — localiser la frontière (comme pour `Neuron Express 2D-0`) puis choisir
   les points de part et d'autre pour forcer chaque bit.

La contrainte « pas deux fois la même paire d'affilée » empêche la stratégie triviale qui
consisterait à marteler un point qui renvoie 0 ou 1 : il faut varier légèrement les entrées.

## Solution

Séquence gagnante, telle qu'observée sur l'instance (les extrêmes du domaine suffisent) :

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

Point important : les huit tirages doivent être **consécutifs** dans la fenêtre glissante ;
un test raté décale la fenêtre et il faut refaire la séquence. C'est pour cela que le setup
« quatre points cardinaux + quatre points extrêmes » est préférable à une recherche adaptative
au milieu de la séquence.

## Flag

```
academy{2d_n3ur0n_m3t_dadc9561}
```

## Sources

- https://shukularuni.neocities.org/guide/ctf/picoctf/ai/Neuron_Meet_2D-0
- https://shukularuni.neocities.org/guide/ctf/picoctf/ai/
- https://learn.cylabacademy.org/library/772
