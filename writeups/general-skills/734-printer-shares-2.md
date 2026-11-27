# 734 — Printer Shares 2

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

## Énoncé

« A Secure Printer is now in use. I'm confident no one can leak the message again... or can you? »

Suite de *Printer Shares* : le service expose du partage de fichiers SMB, et il faut retrouver le
flag malgré le durcissement annoncé.

## Analyse

### Énumération anonyme
```bash
smbclient -L //<HOST> -p <PORT> -N
```

L'énumération sans identifiants fonctionne — première faiblesse, et elle est volontaire. Deux
partages ressortent :

- `shares` — public, accessible en invité ;
- `secure-shares` — avec la description « Printer for internal usage only ».

Une tentative d'accès direct au second échoue :

```bash
smbclient //<HOST>/secure-shares -p <PORT> -N
# NT_STATUS_ACCESS_DENIED
```

Le durcissement, c'est ça : le partage n'est pas supprimé, il est protégé par authentification.

### Fouiller le partage public
```bash
smbclient //<HOST>/shares -p <PORT> -N
# prompt OFF
# recurse ON
# mget *
# exit
```

Le partage contient plusieurs fichiers. `content.txt` et `kafka.txt` sont des **leurres** : ils
contiennent du texte plausible, sans rapport avec l'objectif. C'est une technique classique de
bruitage — elle coûte du temps à qui lit tout.

`notification.txt` donne en revanche l'indice décisif : un utilisateur nommé **joe** utilise encore
le **mot de passe par défaut** de l'imprimante. Autrement dit, `secure-shares` est bien protégé, mais
par un secret faible et connu : il suffit de le casser avec une wordlist.

### Le problème des outils
Les outils de force brute classiques déçoivent ici :

- **`hydra`** ne sait faire du SMB qu'en **SMBv1** pour ce module ; le service ne l'accepte pas (ou
  la négociation échoue), d'où des erreurs peu lisibles plutôt que des échecs d'authentification.
- **`ncrack`** échoue également sur cette cible, pour des raisons de négociation de protocole
  similaires.

Ce qui fonctionne :

- **NetExec** (`nxc`), qui gère SMB2/3 et le décodage des mots de passe correctement :
  `nxc smb <HOST> --port <PORT> -u 'joe' -p rockyou.txt` ;
- une boucle **`smbclient`** qui teste chaque mot de passe de la liste :

  ```bash
  while read p; do
    smbclient //<HOST>/secure-shares -p <PORT> -U "joe%$p" -c 'ls' >/dev/null 2>&1 && echo "$p" && break
  done < rockyou.txt
  ```

Le mot de passe trouvé est **popcorn**. Un mot du dictionnaire, sans mutation : le mot de passe
« par défaut » de l'imprimante est en réalité le mot de passe constructeur jamais changé.

## Solution

### Déroulé complet
```bash
# 1. énumération
smbclient -L //<HOST> -p <PORT> -N

# 2. récupération du partage public
smbclient //<HOST>/shares -p <PORT> -N
#   ls ; prompt OFF ; recurse ON ; mget * ; exit
cat notification.txt

# 3. cassage du mot de passe de joe
nxc smb <HOST> --port <PORT> -u 'joe' -p /usr/share/wordlists/rockyou.txt --ignore-pw-decoding

# 4. accès au partage protégé
smbclient //<HOST>/secure-shares -p <PORT> -U 'joe%popcorn'
#   ls ; get flag.txt ; exit
cat flag.txt
```

### Points d'attention sur les commandes
- `--ignore-pw-decoding` évite que NetExec interprète les entrées de la wordlist comme des chaînes
  échappées ; sur rockyou, certaines séquences seraient altérées avant l'envoi.
- `-U 'joe%popcorn'` : le format `utilisateur%motdepasse` de `smbclient`. Sans le `%`, le mot de passe
  est demandé de façon interactive, ce qui casse une boucle automatisée.
- `-c 'ls'` comme test de succès : on ne cherche pas à lire un fichier à chaque tentative, seulement à
  savoir si l'authentification passe. C'est beaucoup plus rapide.

### Pourquoi ça marche
SMB distingue deux couches : l'**authentification** (identité) et l'**autorisation** (droit de lire
ce partage). Le challenge durcit la première en exigeant un compte, mais celui-ci a un mot de
passe trivial. La protection réelle d'un partage ne dépend donc pas de la présence d'un login, mais
de la robustesse du secret derrière — et un mot du dictionnaire, non modifié, ne résiste pas à
rockyou en quelques secondes. Le leurre des fichiers parasites, lui, ne protège rien : il exploite
seulement le temps de l'analyste.

## Pièges

- **S'acharner avec `hydra`** : une erreur de protocole et non un refus d'authentification signale un
  problème de version SMB, pas un mauvais mot de passe. Basculer sur NetExec ou `smbclient`.
- **`--ignore-pw-decoding`** : sans cette option, certains candidats sont altérés avant l'envoi, ce
  qui produit des faux négatifs impossibles à diagnostiquer.
- **Port** : toujours `-p <PORT>` avec `smbclient` (et `--port` avec `nxc`), sinon on part sur le 445.

## Flag

Flag validé sur la plateforme (valeur non conservée).
