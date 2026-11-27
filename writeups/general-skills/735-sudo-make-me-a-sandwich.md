# 735 — SUDO MAKE ME A SANDWICH

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

## Énoncé
« Can you read the flag? I think you can! »

Accès SSH à la machine du challenge, avec un `flag.txt` dans le répertoire de l'utilisateur. Le titre
est un indice appuyé : il y a une règle `sudo` exploitable, et le sandwich est une métaphore de
l'élévation de privilèges.

## Analyse

### L'énumération de base
```bash
ssh ctf-player@<HOST> -p <PORT>
id
ls -la
sudo -l
```

`ls` montre `flag.txt`, mais sa lecture directe est refusée : le fichier appartient à `root` et n'est
pas lisible par `ctf-player`. Sans le sudo, le challenge s'arrête là.

`sudo -l` est **la** commande du challenge :

```
(ALL) NOPASSWD: /bin/emacs
```

Trois informations :

- l'utilisateur peut exécuter `/bin/emacs` **en tant que root** ;
- `NOPASSWD` : pas de mot de passe à fournir ;
- le chemin est **précis** : c'est bien `/bin/emacs` qui est autorisé, pas « un éditeur ».

### Pourquoi un éditeur est une faille
`emacs` n'est pas seulement un éditeur de texte : c'est un environnement d'exécution complet. Il peut
lancer des processus, évaluer du code Lisp, ouvrir un terminal. Exécuté en root, il offre donc un
shell root — c'est un cas d'école de la famille **GTFOBins** : tout binaire légitime capable de lire
un fichier ou de lancer une commande devient une porte dérobée dès qu'il est autorisé via `sudo`.

Deux voies possibles, au choix :

1. **la plus directe** — `sudo /bin/emacs flag.txt` ouvre simplement le fichier en root et l'affiche.
   Pas besoin de shell : le programme a déjà les droits nécessaires pour lire le fichier.
2. **la plus générale** — obtenir un shell root, utile si l'on veut fouiller au-delà du flag.

## Solution

### Voie directe
```bash
sudo /bin/emacs flag.txt
```
Le fichier s'ouvre dans emacs, avec les droits de root. Le contenu du buffer est le flag. On quitte
avec `C-x C-c`.

Cette voie fonctionne même sans terminal interactif complet, et c'est celle qui coûte le moins
d'étapes : on ne cherche pas à élever ses privilèges, on demande à un programme privilégié de faire
la lecture à notre place.

### Voie shell — interactif
```bash
sudo /bin/emacs -Q -nw
# dans emacs : M-x term  (ou M-x shell)
cat /home/ctf-player/flag.txt
```

`M-x term` ouvre un terminal dans un buffer emacs ; le processus lancé hérite des privilèges du
parent, donc de root. `-Q` évite de charger la configuration utilisateur, `-nw` force le mode
terminal (pas de fenêtre graphique).

### Voie shell — non interactif
Sans PTY (connexion scriptée, pas de terminal alloué), les voies interactives échouent. On utilise
alors l'évaluation batch :

```bash
sudo emacs -Q --batch --eval \
  '(with-temp-buffer (insert-file-contents "/home/ctf-player/flag.txt") (message "%s" (buffer-string)))'
```

Ce one-liner est intéressant à comprendre : `--batch` empêche emacs d'ouvrir un terminal, `--eval`
exécute une expression Lisp, `with-temp-buffer` crée un buffer jetable, `insert-file-contents` lit le
fichier **avec les droits du processus** (root), et `message` l'affiche sur la sortie d'erreur. Rien
n'est interactif, et le résultat arrive directement dans le terminal.

### Pourquoi ça marche
`sudo` autorise l'exécution d'un **binaire** avec les privilèges de la cible, pas une action précise.
La règle `NOPASSWD: /bin/emacs` ne dit pas « ouvrir un fichier en lecture » : elle dit « exécuter
emacs en root ». Or emacs est Turing-complet et peut lancer n'importe quel processus. La règle
accorde donc, en pratique, un accès root complet. C'est la raison pour laquelle les bonnes pratiques
`sudo` interdisent les éditeurs, les pagers (`less`, `more`), les interpréteurs et les gestionnaires
de fichiers : ce sont tous des binaires qui peuvent en lancer d'autres.

## Pièges
- **`sudo emacs` sans chemin** : la règle porte sur `/bin/emacs`. Si le `PATH` résout `emacs` vers un
  autre binaire, `sudo` refuse. Utiliser le chemin exact.
- **Pas de PTY** : `sudo emacs` en mode interactif échoue avec « terminal is not fully functional ».
  La variante `--batch` est la solution, et c'est souvent le seul chemin en environnement scripté.
- **Chercher un fichier lisible ailleurs** : le flag est bien `flag.txt` dans le home de
  `ctf-player` ; inutile de fouiller `/root`, on n'y a pas accès autrement que via emacs.
- **Confondre lecture et copie** : `sudo cp flag.txt /tmp/` ne marche pas — `cp` n'est pas dans la
  règle sudo. C'est bien emacs qu'il faut utiliser.
- **Quitter emacs** : `C-x C-c`. Rester bloqué dans l'éditeur donne l'impression que la session est
  gelée.

## Flag

Flag validé sur la plateforme (valeur non conservée).
