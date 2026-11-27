# 189 — Magikarp Ground Mission

**Événement** : picoCTF 2021 · **Catégorie** : Général Skills

## Énoncé

« Do you know how to move between directories and read files in the shell? Start the container, ssh to it, and then ls once connected to begin. »

Le challenge fournit un accès SSH à un conteneur : utilisateur `ctf-player`, mot de passe communiqué par la plateforme (un identifiant court du type `6d448c9c`), port variable d'une instance à l'autre. Le flag est découpé en trois fichiers, chacun accompagné d'un fichier d'instructions qui indique où trouver le suivant.

## Analyse

La compétence testée est la navigation dans l'arborescence Unix, pas l'exploitation :

- `ls` et `ls -a` pour lister, y compris les entrées commençant par un point ;
- `cd ..` pour remonter, `cd /` pour aller à la racine, `cd ~` pour revenir au répertoire personnel ;
- `cat` pour lire un fichier.

Le répertoire d'arrivée contient `1of3.flag.txt` et `instructions-to-2of3.txt`. Les instructions envoient vers la racine du système, où se trouve le troisième fragment, puis vers le répertoire personnel pour le deuxième. L'ordre des fragments n'est donc pas l'ordre des répertoires : il faut suivre les fichiers d'instructions, pas raisonner sur l'arborescence.

Le port SSH n'est pas le 22 : la plateforme attribue un port haut, et la connexion échoue en `Connection refused` si on l'omet.

## Solution

### 1. Se connecter

```bash
ssh ctf-player@venus.picoctf.net -p 50713
# mot de passe fourni par la plateforme
```

Le `-p` est obligatoire, et la première connexion demande de valider l'empreinte de l'hôte : on répond `yes`.

### 2. Premier fragment

```bash
pwd
ls
cat 1of3.flag.txt
```

`pwd` confirme le répertoire courant et `ls` montre les deux fichiers. Le premier fragment s'ouvre sur le préfixe de flag de l'événement, suivi du début d'un mot en leetspeak : on note le morceau tel qu'il s'affiche et on garde le préfixe avec.

### 3. Suivre les instructions

```bash
cat instructions-to-2of3.txt
```

Le fichier indique d'aller à la racine. On obéit littéralement :

```bash
cd /
ls -a
cat 3of3.flag.txt
```

Le troisième fragment se termine par l'accolade fermante du flag. C'est le seul repère qui confirme qu'on est bien au bout de la chaîne.

### 4. Revenir pour le deuxième fragment

```bash
cd ~
cat 2of3.flag.txt
```

Le deuxième fragment est le plus piégeux : il contient des barres obliques inversées et des soulignés. Il faut le recopier **caractère par caractère**, sans le passer dans un `echo` ou un `printf`, qui interpréteraient les échappements et casseraient la valeur.

### 5. Assembler

On concatène dans l'ordre 1, 2, 3 — l'ordre des fichiers, pas l'ordre des répertoires visités — et on colle le résultat sur la plateforme.

```bash
# vérification de l'ordre : les trois morceaux doivent former une seule chaîne
cat 1of3.flag.txt 2of3.flag.txt 3of3.flag.txt   # NE PAS utiliser : ajoute des retours à la ligne
```

### Pourquoi ça marche

Chaque fragment est un fichier texte ordinaire, et les instructions disent où aller. Le challenge ne teste que la lecture et le déplacement : il suffit d'exécuter les commandes dans l'ordre indiqué et de concaténer les morceaux dans l'ordre des numéros.

## Pièges

- **Ordre des répertoires** : le troisième fragment est à la racine et le deuxième dans le répertoire personnel ; suivre `cd ..` de proche en proche ne donne pas le bon ordre.
- **`ls` sans `-a`** : un nom caché peut disparaître du listing et faire croire que le fragment manque.
- **Échappements du fragment 2** : les barres obliques inversées font partie du flag ; un `echo` les mange.
- **Concaténation avec `cat`** : les sauts de ligne entre fichiers s'insèrent dans la valeur ; il faut recopier les morceaux à la main ou utiliser `tr -d '\n'`.
- **Port SSH** : sans `-p`, on tape sur le 22 du conteneur et la connexion est refusée.
