# 279 — Lookey here

**Événement** : picoCTF 2022 · **Catégorie** : Forensics

## Énoncé

« Des attaquants ont caché des informations dans une très grande masse de données par le passé, et ils le font peut-être encore. » L'archive fournie contient un unique fichier texte volumineux (`anthem.flag.txt`), présenté comme un long texte narratif.

## Analyse

Le challenge appartient à la famille « aiguille dans une botte de foin » : le flag est en **clair**, sans encodage ni stéganographie, simplement noyé dans un volume de texte qui rend la lecture visuelle impraticable. La difficulté est donc purement le volume, pas la technique.

Réflexes de triage sur un fichier texte inconnu :

- `file` pour confirmer le type (ASCII ou UTF-8, éventuellement signalé « with very long lines ») ;
- `wc -c` et `wc -l` pour mesurer l'ordre de grandeur ;
- recherche directe d'un motif connu plutôt que lecture.

Le point important est que le flag n'est pas sur une ligne à lui : il est **concaténé à la fin d'une phrase** du récit. Un `head`, un `tail` ou une lecture des premières pages ne le montrent donc jamais.

## Solution

### 1. Triage

```bash
file anthem.flag.txt
wc -l anthem.flag.txt
wc -c anthem.flag.txt
```

`file` confirme un fichier texte ; les deux `wc` donnent une idée du rapport entre nombre de lignes et taille, utile pour repérer des lignes anormalement longues.

### 2. Recherche du motif

```bash
grep -ai "pico" anthem.flag.txt
```

`-a` force le traitement comme texte (le fichier peut contenir des octets non imprimables qui feraient basculer `grep` en mode binaire), `-i` ignore la casse. La ligne retournée est une phrase du récit qui se termine par le flag.

### 3. Isolation du motif

Comme la ligne est longue, on n'affiche que la correspondance :

```bash
grep -ao "[A-Za-z0-9_]*{[^}]*}" anthem.flag.txt
```

Le motif générique « préfixe alphanumérique + accolades » évite de dépendre du préfixe exact de l'événement et isole la valeur proprement.

### 4. Variantes utiles

```bash
strings -n 8 anthem.flag.txt | grep -i pico
grep -rn "pico" .
```

La première enlève le bruit des chaînes trop courtes ; la seconde cherche dans tout le répertoire si l'archive contient d'autres fichiers que celui annoncé.

### Pourquoi ça marche

Le flag est écrit en clair dans le récit ; aucune transformation ne le protège. La recherche textuelle suffit donc, à condition de traiter le fichier comme du texte et de ne pas se laisser arrêter par la longueur des lignes.

## Pièges

- **Lire le fichier** : quelques centaines de kilo-octets de récit, la lecture est le piège à temps.
- **`head` ou `tail`** : le flag est au milieu d'une ligne, pas aux extrémités du fichier.
- **`grep` sans `-a`** : sur un fichier contenant des octets non imprimables, `grep` affiche « binary file matches » au lieu de la ligne.
- **`grep` sans `-o`** : la ligne entière est recrachée et le flag se perd dans le texte ; `-o` n'affiche que le motif.
- **Confondre volume et chiffrement** : rien n'est encodé ici ; chercher un décodage fait perdre du temps.

## Flag

Flag validé sur la plateforme (valeur non conservée).
