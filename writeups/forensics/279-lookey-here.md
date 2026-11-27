# 279 — Lookey here

**Événement** : picoCTF 2022 · **Catégorie** : Forensics · **Auteur** : non précisé dans les sources consultées

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

« Des attaquants ont caché des informations dans une très grande masse de données par le
passé, et ils le font peut-être encore. » L'archive fournie contient un unique fichier texte
volumineux (`anthem.flag.txt`), présenté comme un long texte narratif.

## Analyse

Le challenge appartient à la famille « aiguille dans une botte de foin » : le flag est en
**clair**, sans encodage ni stéganographie, simplement noyé dans un volume de texte qui rend
la lecture visuelle impraticable. La difficulté est donc purement le volume, pas la technique.

Réflexes de triage sur un fichier texte inconnu :

- `file` pour confirmer le type (ASCII/UTF-8, éventuellement « with very long lines ») ;
- `wc -c` / `wc -l` pour mesurer l'ordre de grandeur ;
- recherche directe d'un motif connu (`pico`, `CTF`, `flag`) plutôt que lecture.

## Solution

```bash
file anthem.flag.txt
wc -l anthem.flag.txt
grep -ai "pico" anthem.flag.txt
```

`grep` retourne une ligne du style `we think that the men of picoCTF{...}` : le flag est
**concaténé au texte narratif**, ce qui explique qu'une simple lecture des premières lignes
ou un `head` le rate complètement.

Variantes utiles :

```bash
grep -rEao "picoCTF\{[^}]*\}" .
strings -n 8 anthem.flag.txt | grep -i pico
```

En cas de fichier binaire ou d'encodage mixte, `grep -a` (traiter le binaire comme du texte)
et `-o` (n'afficher que le motif) sont les deux options qui font gagner du temps.

## Flag

```
picoCTF{gr3p_15_@w3s0m3_58f5c024}
```

## Sources

- https://ctftime.org/writeup/33098
- https://ctftime.org/writeup/32911
