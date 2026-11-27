# 740 — Piece by Piece

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

## Énoncé

« After logging in, you will find multiple file parts in your home directory. These parts need to be combined and extracted to reveal the flag. »

Un accès SSH à la machine du challenge est fourni : tout se joue dans le répertoire personnel de l'utilisateur `ctf-player`.

## Analyse

Après connexion, le `ls -la` montre un `instructions.txt` et une série de fichiers dont le nom commence par `part_`. L'énoncé les appelle des « file parts » : ce sont les morceaux d'une **archive ZIP unique**, découpée en tranches pour être distribuée.

`instructions.txt` donne les trois informations utiles : la cible est un ZIP, il faut recombiner les morceaux avec les commandes Linux standard, et l'archive est protégée par le mot de passe `supersecret`.

La recombination se fait avec `cat` — le nom vient de *concatenate*, et c'est exactement l'opération : recoller des flux d'octets bout à bout. `cat part_* > combined.zip` produit un fichier qui, octet pour octet, est identique au ZIP d'origine.

Le seul vrai point d'attention est l'**ordre**. Le shell développe le glob `part_*` dans l'ordre de tri de la locale courante, c'est-à-dire alphabétique : correct pour `part_aa`, `part_ab`, … ou `part_01`, `part_02`, …, mais faux dès que la numérotation n'est pas nulle-paddée, puisque `part_10` se trie avant `part_2`. On vérifie donc toujours l'expansion réelle du glob avant de concaténer.

Enfin, `file` sert de garde-fou : un ZIP valide doit être reconnu comme tel. Si l'outil répond `data`, c'est que les tranches sont dans le mauvais ordre ou incomplètes.

## Solution

### 1. Se connecter et lire les instructions

```bash
ssh ctf-player@<HOST> -p <PORT>
ls -la
cat instructions.txt
```

### 2. Contrôler l'ordre des morceaux

```bash
ls -v *part*
echo part_*
```

`ls -v` applique un tri « version », donc numérique : si l'ordre affiché diffère de celui de `echo part_*`, il ne faut pas utiliser `cat part_*` tel quel mais trier explicitement.

### 3. Recombiner et vérifier le résultat

```bash
cat part_* > combined.zip
file combined.zip
ls -l combined.zip part_*
```

`file` doit répondre `Zip archive data`, éventuellement suivi de la mention `at least v2.0 to extract`. Si la réponse est `data` ou `ASCII text`, l'ordre ou le jeu de morceaux est faux : on recommence avec une liste triée à la main.

```bash
cat $(ls part_* | sort -V) > combined.zip
file combined.zip
```

La taille cumulée donne aussi une indication : la somme des morceaux doit égaler exactement la taille du fichier produit.

### 4. Extraire et lire

```bash
unzip -P supersecret combined.zip
ls -la
cat flag.txt
```

L'option `-P` passe le mot de passe en argument, ce qui évite le prompt interactif et rend la commande rejouable dans un script. Le flag apparaît dans le fichier texte extrait.

### Pourquoi ça marche

Un ZIP est un format conteneur : son en-tête et son répertoire central se trouvent à la **fin** du fichier. Un découpage en tranches ne modifie pas le contenu, seulement la position des octets ; recoller les tranches dans le bon ordre restitue le fichier d'origine à l'identique, et l'archive redevient lisible sans aucune étape de reconstruction. Le mot de passe, lui, relève du chiffrement appliqué par entrée : `unzip -P` se contente de le fournir au déchiffrement local, il n'y a rien à casser.

## Pièges

- **Le tri du glob.** `part_1 part_10 part_2` : sans padding, le tri alphabétique casse l'archive. L'erreur ne se voit qu'au `file` final, pas avant.
- **La concaténation en mode texte.** Un éditeur ou un copier-coller peut altérer les octets binaires ; `cat` en shell est sûr. On évite les redirections dans le désordre et les `cat` partiels suivis d'un `>>`.
- **Le mot de passe tapé à la main.** `supersecret` est simple, mais un `unzip` interactif redemande en cas de faute ; `-P` rend l'opération non interactive.
- **Le `flag.txt` déjà présent.** Vérifier qu'après extraction on lit bien le fichier produit par `unzip`, et pas un homonyme resté dans le répertoire.

## Flag

Flag validé sur la plateforme (valeur non conservée).
