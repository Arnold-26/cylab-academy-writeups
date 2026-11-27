# 35 — Based

**Événement** : picoCTF 2019 · **Catégorie** : General Skills · **Auteur** : Alex Fulton/Daniel Tunitits

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

Un service réseau demande de convertir des données entre plusieurs bases (binaire, octal,
hexadécimal) pour reconstituer des mots. La validation se fait en trois questions, avec un temps
limité (environ 45 secondes), d'où la nécessité d'automatiser.

## Analyse

Le service énonce un mot cible puis quatre à cinq valeurs numériques séparées par des espaces,
chacune étant le code ASCII d'un caractère dans une base donnée :

- une suite de `0`/`1` de longueur 8 : base 2 ;
- des valeurs dont le chiffre maximal est `7` (ex. `146 141 154 143 157 156`) : base 8 ;
- une chaîne hexadécimale compacte (ex. `737472656574`) : base 16.

La difficulté n'est pas la conversion mais la vitesse : la résolution manuelle dépasse le délai. Le
service affiche par ailleurs le mot attendu avant la question (comportement de debug), ce qui
permet aussi de répondre sans décoder.

## Solution

1. Se connecter pour observer le format :

```bash
nc jupiter.challenges.picoctf.org 29221
```

2. Conversion manuelle des trois familles :

```python
"".join(chr(int(x, 2)) for x in "01100011 01101000 01100001 01101001 01110010".split())
# chair
"".join(chr(int(x, 8)) for x in "146 141 154 143 157 156".split())
# falcon
bytes.fromhex("737472656574").decode()
# street
```

3. Automatiser avec pwntools pour tenir dans le délai : lire la ligne de question, décoder,
   répondre, répéter. Squelette issu des writeups publics :

```python
from pwn import *
io = remote("jupiter.challenges.picoctf.org", 29221)
# lire la valeur, choisir la base (2, 8, 16), décoder, sendlineafter(b"Input:\n", reponse)
```

4. Récupérer la dernière ligne renvoyée par le service : elle contient le flag.

## Flag

`picoCTF{learning_about_converting_values_8e70d435}`

## Sources

- https://raw.githubusercontent.com/Dvd848/CTFs/master/2019_picoCTF/Based.md — énoncé, exemples binaire/octal/hex, script pwntools complet et flag affiché
- https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/master/picoCTF_2019/General_Skills/Based.md — énoncé, indices et version allégée du script (mention du mot affiché par le service)
