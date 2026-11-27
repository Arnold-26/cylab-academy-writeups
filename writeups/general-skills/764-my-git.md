# 764 — MY GIT

**Événement** : picoCTF 2026 · **Catégorie** : Général Skills

## Énoncé

> I have built my own Git server with my own rules! You want the flag - make sure to push the flag.
> Only `flag.txt` pushed by root (name: root, email: root@picoctf) will be updated with the flag.

L'instance expose un dépôt Git en HTTP et un mot de passe sur la page du challenge. Un hook côté
serveur surveille les pushes : il ne rend le flag que si `flag.txt` arrive dans un commit attribué
à `root <root@picoctf>`.

## Analyse

On commence par regarder ce que le serveur contrôle vraiment. Un objet commit Git est du texte
structuré, entièrement fabriqué par le client :

```
tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904
parent 8a1c0f0c3e1d2b4a5c6d7e8f90123456789abcde
author root <root@picoctf> 1710000000 +0000
committer root <root@picoctf> 1710000000 +0000

add flag
```

Les lignes `author` et `committer` sont écrites au moment du `git commit`, à partir de
`user.name`, `user.email` et de l'horloge locale. Aucune de ces valeurs n'est vérifiée par le
protocole : la signature GPG d'un commit est optionnelle, et un hook qui lit le nom et le courriel
ne voit que la chaîne déclarée.

Le contrôle d'identité est donc un contrôle de forme. Il suffit de se déclarer root dans la
configuration du dépôt cloné pour que le hook — qui teste la chaîne, pas une clé — considère le
commit comme légitime. C'est l'équivalent Git d'un serveur web qui ferait confiance à un en-tête
`X-User: admin`.

Deuxième point : le hook porte sur le **chemin**. C'est `flag.txt` à la racine de l'arbre qui
l'intéresse. Un fichier dans un sous-dossier, ou portant un autre nom, ne déclenche rien.

## Solution

1. Cloner le dépôt avec les identifiants de la page :

```bash
git clone http://<HOST>:<PORT>/repo.git
# Username / Password demandés : ceux de l'instance
cd repo
```

2. Déclarer l'identité attendue, localement au dépôt (rien ne fuit vers la configuration
   globale) :

```bash
git config user.name root
git config user.email root@picoctf
git config --get user.name    # root
git config --get user.email   # root@picoctf
```

3. Vérifier l'identité que Git utilisera réellement, avant de committer :

```bash
git var GIT_AUTHOR_IDENT
# root <root@picoctf> <horodatage> +0000
```

4. Créer le fichier, committer, puis relire l'objet produit :

```bash
printf 'pending\n' > flag.txt
git add flag.txt
git commit -m 'add flag'
git cat-file -p HEAD
# author root <root@picoctf> ...
# committer root <root@picoctf> ...
```

`git cat-file -p HEAD` est le contrôle décisif : on lit exactement ce que le serveur lira.

5. Pousser sur la branche par défaut du dépôt :

```bash
git push origin HEAD
```

Le hook réécrit alors `flag.txt` avec le vrai flag et le renvoie dans la sortie du push. Si la
sortie a défilé, un `git pull` récupère la version réécrite du fichier côté serveur.

## Pièges

- **Configuration globale contre locale.** Un `user.name` présent dans `~/.gitconfig` est écrasé
  par la valeur locale, et l'inverse est vrai aussi. On ne suppose jamais :
  on vérifie avec `git var`.
- **Auteur et committer.** Les deux champs existent et un hook peut n'en lire qu'un. On aligne les
  deux, et au besoin on force l'environnement :
  `GIT_COMMITTER_NAME=root GIT_COMMITTER_EMAIL=root@picoctf git commit -m 'add flag'`.
- **`git commit --amend`** conserve l'auteur d'origine et ne réécrit que le committer : après un
  amend, on relit `git cat-file -p HEAD` au lieu de croire l'identité corrigée.
- **Fichier vide.** Un `flag.txt` vide reste valide pour Git, mais un hook qui teste la présence de
  contenu peut l'ignorer. On écrit une ligne neutre pour lever l'ambiguïté.
- **Refus au push.** Le mot de passe est demandé au push autant qu'au clone ; si on l'inline dans
  l'URL, il faut encoder les caractères réservés (`%40` pour `@`).

**Pourquoi ça marche.** Git ne signe rien par défaut : le couple (nom, courriel) est une
déclaration du client, transportée telle quelle dans le pack. Le serveur n'a aucun moyen de la
recouper avec un compte, puisqu'aucune authentification par clé n'est exigée ici. Le hook fait donc
confiance à une donnée non authentifiée : la faille est dans le modèle de confiance, pas dans la
configuration du serveur.
