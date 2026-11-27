# 766 — Undo

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

> Can you reverse a series of Linux text transformations to recover the original flag? Start by
> searching for the flag here.

Un service TCP affiche un flag transformé et un indice décrivant la transformation ; il faut saisir
la commande Linux qui l'inverse.

## Analyse

Chaque étape fournit une transformation **et son nom** en clair (« Base64 encoded the string »,
« Reversed the text », « Replaced underscores with dashes », « Replaced curly braces with
parentheses », « Applied ROT13 to letters »). Il n'y a donc rien à deviner depuis le texte : il
suffit de connaître la commande inverse. Toutes ces transformations sont réversibles sans clé, et
l'enchaînement des pipes se rejoue simplement à l'envers. La sortie est validée étape par étape.

## Solution

1. Se connecter et lire l'indice de chaque étape : `nc <HOST> <PORT>`.
2. Saisir la commande inverse (une seule commande, sans `echo`) :

| Transformation | Indice | Commande inverse |
|---|---|---|
| Base64 | « Base64 encoded the string » | `base64 -d` |
| Texte inversé | « Reversed the text » | `rev` |
| Tirets → underscores | « Replaced underscores with dashes » | `tr '-' '_'` |
| Parenthèses → accolades | « Replaced curly braces with parentheses » | `tr '()' '{}'` |
| ROT13 | « Applied ROT13 to letters » | `tr A-Za-z N-ZA-Mn-za-m` |

3. Une fois toutes les transformations annulées, le résultat commence par `picoCTF{` : le serveur
   rend le flag.

## Flag

```
picoCTF{Revers1ng_t3xt_Tr4nsf0rm@t10ns_a12e8886}
```

Flag complet publié par le writeup Cdenton (transcription de la session) ; préfixe
`picoCTF{Revers1ng_t3xt_Tr4nsf0rm@t10ns_` corroboré par picoCTF Solutions.

## Sources

- [picoCTF Solutions — Undo (picoCTF 2026)](https://picoctfsolutions.com/picoctf-2026-undo)
- [Cdenton — picoCTF 2026 writeup](https://cdenton1.github.io/2026/03/19/picoCTF-26.html)
