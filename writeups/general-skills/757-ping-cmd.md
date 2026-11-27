# 757 — ping-cmd

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

> Can you make the server reveal its secrets? It seems to be able to ping Google DNS, but what
> happens if you get a little creative with your input?

Une interface web accepte une adresse IP et exécute un `ping` dessus.

## Analyse

L'application concatène l'entrée utilisateur dans une commande shell (`ping <input>`) sans
assainissement : les métacaractères (`;`, `|`, backticks) permettent d'enchaîner une commande
arbitraire. L'injection est « in-band » : la sortie de la commande injectée est renvoyée dans la
page, après les statistiques du ping. Attention au piège classique : `flag.txt` n'est pas à la
racine mais dans le répertoire de travail du script.

## Solution

1. Reconnaître le point d'injection : le champ IP part directement au shell.
2. Lister le répertoire courant, puis lire les fichiers utiles :

```bash
8.8.8.8 ; ls
8.8.8.8 ; cat script.txt      # confirme la façon dont l'entrée est traitée
8.8.8.8 ; cat flag.txt
```

3. La sortie de `cat flag.txt` s'affiche dans la réponse HTTP.

## Flag

```
picoCTF{p1nG_c0mm@nd_3xpL0it_su33essFuL_...}
```

Préfixe publié par picoCTF Solutions. Deux writeups publient des suffixes différents
(`..._a9326567` chez root-ninja, `..._e003709d` chez Cdenton) : le suffixe n'est pas recopié ici,
flag complet non conservé.

## Sources

- [picoCTF Solutions — Ping-Cmd (picoCTF 2026)](https://picoctfsolutions.com/picoctf-2026-ping-cmd)
- [root-ninja/picoCTF-write-ups-2026 — ping-cmd.md](https://github.com/root-ninja/picoCTF-write-ups-2026/blob/main/ping-cmd.md)
- [Cdenton — picoCTF 2026 writeup](https://cdenton1.github.io/2026/03/19/picoCTF-26.html)
