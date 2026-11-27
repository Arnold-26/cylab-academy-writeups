# 189 — Magikarp Ground Mission

**Événement** : picoCTF 2021 · **Catégorie** : General Skills · **Auteur** : non documenté

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

Le challenge fournit un accès SSH à un conteneur : « Do you know how to move between directories
and read files in the shell? Start the container, ssh to it, and then ls once connected to begin ».
L'identifiant est `ctf-player` avec un mot de passe communiqué par la plateforme (par exemple
`6d448c9c`), le port variant selon l'instance.

## Analyse

Le flag est découpé en trois fichiers, chacun accompagné d'un fichier d'instructions indiquant où
chercher le suivant. La compétence testée est la navigation dans l'arborescence Unix :

- `ls` / `ls -a` pour lister (y compris les fichiers cachés) ;
- `cd ..` pour remonter, `cd /` pour aller à la racine, `cd ~` pour revenir au répertoire
  personnel ;
- `cat` pour lire un fichier.

Le point d'entrée contient `1of3.flag.txt` et `instructions-to-2of3.txt`. Les instructions
envoient vers la racine du système, où se trouve le troisième fragment, puis vers le répertoire
personnel pour le deuxième. L'ordre des fragments n'est donc pas l'ordre des répertoires : il faut
suivre les fichiers d'instructions.

## Solution

1. Se connecter :

```bash
ssh ctf-player@venus.picoctf.net -p 50713
# mot de passe fourni par la plateforme
```

2. Lister et lire le premier fragment :

```bash
ls
# 1of3.flag.txt  instructions-to-2of3.txt
cat 1of3.flag.txt
# picoCTF{xxsh_
```

3. Suivre les instructions (aller à la racine), puis chercher le troisième fragment :

```bash
cd /
ls -a
cat 3of3.flag.txt
# 5190b070}
```

4. Revenir dans le répertoire personnel (`cd ~`) pour le deuxième fragment :

```bash
cat 2of3.flag.txt
# 0ut_0f_\/\/4t3r_
```

5. Concaténer dans l'ordre 1, 2, 3 : `picoCTF{xxsh_` + `0ut_0f_\/\/4t3r_` + `5190b070}`.

Le fragment contient des barres obliques inversées (`\/\/`) qui font partie du flag : elles
doivent être recopiées telles quelles.

## Flag

`picoCTF{xxsh_0ut_0f_\/\/4t3r_5190b070}`

## Sources

- https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/General%20Skills/Magikarp%20Ground%20Mission/README.md — énoncé, identifiants, contenu des trois fragments et assemblage final
