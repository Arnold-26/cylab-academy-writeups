# 759 — Printer Shares

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

## Énoncé

> Oops! Someone accidentally sent an important file to a network printer - can you retrieve it from
> the print server?

Seul outil nécessaire : `smbclient`. Un serveur et un port sont fournis.

## Analyse

### Reconnaître le protocole

« Network printer » et « print server » désignent du partage de fichiers Windows, donc SMB. Le port
fourni confirme : ce n'est pas une interface d'impression web mais un service de fichiers SMB.

### Session nulle

Le serveur accepte une **session nulle** : un bind anonyme, sans identifiants. C'est une
configuration par défaut fréquente sur les anciens serveurs d'impression, où l'énumération des
partages est laissée ouverte. Avec `smbclient`, l'option `-N` supprime l'invite de mot de passe et
permet de lister les partages sans authentification.

La liste révèle un partage applicatif nommé `shares`, à côté du partage d'administration `IPC$`. Ce
dernier est un canal interne SMB, pas un répertoire : la cible est `shares`, là où le fichier imprimé
par erreur a atterri.

### Ce qu'on cherche

Un fichier texte, vraisemblablement nommé `flag.txt`, déposé à la racine du partage. Il est lisible
sans identifiants : l'accès anonyme n'est pas limité en lecture sur ce partage.

## Solution

### 1. Énumérer les partages en anonyme

```bash
sudo apt install -y smbclient
smbclient -L //<HOST> -p <PORT> -N
# Sharename   Type   Comment
# shares      Disk
# IPC$        IPC    IPC Service
```

Le `-p` fixe le port non standard ; sans lui, `smbclient` vise 445 et la connexion échoue.

### 2. Se connecter au partage applicatif

```bash
smbclient //<HOST>/shares -p <PORT> -N
smb: \> recurse ON
smb: \> ls
smb: \> get flag.txt
smb: \> exit
```

Le `recurse ON` évite de rater le fichier s'il n'est pas à la racine du partage.

### 3. Lire le fichier

```bash
cat flag.txt
file flag.txt        # ASCII text : rien à décoder
```

### 4. Variante scriptée

```bash
smbclient //<HOST>/shares -p <PORT> -N -c 'recurse ON; prompt OFF; mget *'
```

`prompt OFF` désactive la confirmation fichier par fichier, ce qui rend le `mget` utilisable en une
seule commande et permet de récupérer l'ensemble du partage d'un coup.

### Pourquoi ça marche

SMB permet à un client de s'authentifier avec un contexte vide : c'est le « null session » hérité des
configurations de partage anonyme. Le serveur ne distingue alors pas un visiteur d'un poste du réseau
interne et sert les fichiers du partage sans contrôle d'accès. L'erreur d'exploitation — un document
envoyé au mauvais destinataire — se double donc d'une erreur de configuration qui rend le partage
lisible par n'importe qui.

## Pièges

- **Oublier `-N`.** Sans cette option, `smbclient` demande un mot de passe et la session anonyme n'est
  jamais tentée.
- **Oublier `-p <PORT>`.** Le service n'écoute pas sur le port SMB standard : la connexion reste en
  timeout et laisse croire que le service est fermé.
- **Viser `IPC$`.** C'est un canal de communication interne, pas un répertoire de fichiers ; le
  document est dans `shares`.
- **Transfert en mode ASCII.** `smbclient` peut traduire les fins de ligne et corrompre le fichier :
  passer en `binary` avant `get` si le contenu semble altéré.
- **Ne lire que la racine du partage.** Un `recurse ON` coûte une commande et évite un faux négatif.
- **Confondre avec un challenge voisin.** « Printer Shares 2 » a un autre flag : le nom du challenge
  doit correspondre à l'instance interrogée.

## Flag

Flag validé sur la plateforme (valeur non conservée).
