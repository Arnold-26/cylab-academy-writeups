# 48 — plumbing

**Événement** : picoCTF 2019 · **Catégorie** : Général Skills · **Auteur** : Alex Fulton/Danny Tunitits

## Énoncé

Un service réseau renvoie un flux continu de lignes sans intérêt (« Not a flag either », « I don't
think this is a flag either », etc.) parmi lesquelles se trouve une seule ligne au format du flag.
L'indice parle de « pipe » et de la nécessité de garder la sortie du programme hors d'un fichier.

## Analyse

On observe d'abord le comportement brut, sans rien filtrer :

```bash
nc <HOST> 7480
```

Le programme écrit énormément de lignes, bien plus que ce qu'un terminal peut afficher : le flag
défile et disparaît du scrollback. Deux stratégies fonctionnent.

- **Rediriger la sortie vers un fichier** (`nc host port > out.txt`) puis chercher dedans. Cela
  oblige à attendre la fermeture de la connexion, puisque `nc` écrit au fil de l'eau mais que le
  fichier n'est complet qu'à la fin : c'est long, et le challenge est calibré pour rendre cette
  attente pénible.
- **Brancher directement `stdout` de `nc` sur `stdin` de `grep`** avec le tube `|`. `grep` ne laisse
  passer que la ligne utile dès qu'elle arrive, sans attendre la fin du flux.

La seconde est la réponse attendue : c'est la composition Unix de base — un programme fait une
chose, le tube assemble les programmes sans les modifier, chacun travaillant en flux. Le flag est
dans le premier bloc de lignes, donc le filtrage en direct le rend en quelques secondes.

## Solution

1. Filtrer le flux en direct sur le motif :

```bash
nc <HOST> 7480 | grep picoCTF
```

2. La commande affiche immédiatement la seule ligne correspondante. `grep` reste bloqué si le
   service continue d'émettre après le flag : `Ctrl+C` suffit, la ligne est déjà sortie.

3. Variantes équivalentes, utiles quand le flux se comporte autrement :

```bash
nc <HOST> 7480 | grep -m1 picoCTF
nc <HOST> 7480 | grep -a --line-buffered picoCTF
nc <HOST> 7480 > out.txt && grep picoCTF out.txt
```

`-m1` arrête `grep` après la première correspondance, ce qui ferme le tube et fait terminer `nc` :
la commande rend la main toute seule.

4. Contrôle du débit, pour comprendre pourquoi le terminal perd la ligne :

```bash
nc <HOST> 7480 | pv > /dev/null
```

`pv` affiche le volume transféré : c'est ce volume qui noie le flag dans le scrollback.

## Pièges

- **Stocker dans un fichier.** La redirection fonctionne, mais la connexion reste ouverte et le
  challenge est conçu pour que l'attente décourage : c'est précisément ce que l'indice déconseille.
- **`grep` sans `-a`.** Si un octet non UTF-8 traverse le flux, `grep` peut le traiter comme du
  binaire et afficher `Binary file matches` au lieu de la ligne. `-a` force le mode texte.
- **Mauvaise casse.** Le motif `picoCTF` est sensible à la casse ; `grep -i` évite de rater la ligne
  si l'énoncé l'écrit différemment.
- **Sortie bufferisée.** Un tube peut bufferiser par blocs et retarder l'affichage :
  `--line-buffered` rétablit un affichage ligne à ligne.
- **Attendre la fin du flux.** Certains services ne ferment jamais la connexion ; il faut savoir
  interrompre la commande une fois la ligne obtenue.

**Pourquoi ça marche.** `grep` lit son entrée standard en flux et écrit les lignes qui correspondent
au motif, sans se soucier de ce que produit le programme en amont. Le tube réalise ce raccordement
au niveau du noyau, sans fichier intermédiaire : le filtrage est donc instantané et indépendant du
volume. C'est la démonstration qu'un outil de filtrage est plus utile qu'un outil de stockage quand
l'information est rare dans un flux dense.
