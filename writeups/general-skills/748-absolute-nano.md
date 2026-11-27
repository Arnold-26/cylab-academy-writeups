# 748 — ABSOLUTE NANO

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

> You have complete power with nano. Think you can get the flag?

Accès SSH à une machine ; l'utilisateur doit élever ses privilèges pour lire `/flag`.

## Analyse

`sudo -l` révèle une règle `NOPASSWD` très étroite : `nano` est autorisé **uniquement** sur
`/etc/sudoers`. Or un éditeur lancé en root sur le fichier de politique de sudo, c'est déjà root :
il suffit d'écrire une règle permissive pour son propre compte. C'est le cas d'école GTFOBins
« éditeur autorisé par sudo » — sudo ne restreint pas ce qu'on écrit dans le fichier.

## Solution

1. Énumérer les droits : `sudo -l` → `nano /etc/sudoers` en `NOPASSWD`.
2. Ouvrir le fichier avec le droit accordé : `sudo nano /etc/sudoers`.
3. En bas du fichier, ajouter une règle pour son utilisateur (`picoplayer`), puis sauver
   (`Ctrl+O`, confirmer le nom) et quitter (`Ctrl+X`) :

```
picoplayer ALL=(ALL) NOPASSWD: ALL
```

4. La règle prend effet immédiatement ; lire le flag : `sudo cat /flag`.

## Flag

```
picoCTF{n4n0_411_7h3_w4y_3dc38f6f}
```

Flag complet publié par le writeup Cdenton (transcription d'exécution) ; préfixe
`picoCTF{n4n0_411_7h3_w4y_` corroboré par picoCTF Solutions.

## Sources

- [picoCTF Solutions — Absolute Nano (picoCTF 2026)](https://picoctfsolutions.com/picoctf-2026-absolute-nano)
- [Cdenton — picoCTF 2026 writeup](https://cdenton1.github.io/2026/03/19/picoCTF-26.html)
- [blz911/picoCTF2026_writeups — General-Skills/Absolute Nano](https://github.com/blz911/picoCTF2026_writeups/blob/main/General-Skills/Absolute%20Nano.md)
