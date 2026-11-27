# 350 — hideme

**Événement** : picoCTF 2023 · **Catégorie** : Forensics

## Énoncé

« Chaque fichier obtient un flag. L'analyste SOC a vu une image être envoyée et renvoyée entre deux personnes. En l'examinant, il s'est rendu compte qu'il y avait plus que ce que l'œil perçoit. »

## Analyse

Le fichier est un PNG (`flag.png`, 512×504, RGBA). Trois vérifications réflexes :

1. **Métadonnées** — `exiftool` signale `Warning: [minor] Trailer data after PNG IEND chunk` : il y a des données après la fin officielle du PNG.
2. **Chaînes** — `strings -n 8` fait apparaître des chemins `secret/` et `secret/flag.png`, signature d'une archive ZIP concaténée.
3. **Signatures** — `binwalk` confirme une archive ZIP à l'offset `0x9B3B`, contenant deux entrées : le dossier `secret/` et `secret/flag.png`.

Technique : « fichier dans le fichier » (polyglotte PNG+ZIP). Le décodeur PNG ignore tout ce qui suit le chunk `IEND`, tandis qu'un décompresseur ZIP retrouve son archive par l'enregistrement de fin de répertoire central, situé à la fin du fichier. Les deux lecteurs peuvent donc coexister sur les mêmes octets.

Le warning d'`exiftool` est la clé du raisonnement : un PNG légitime se termine par un chunk `IEND` et rien d'autre. Toute donnée résiduelle après ce chunk est un conteneur ajouté.

Un PNG est une suite de chunks au format `longueur | type | données | CRC`, terminée par un `IEND` de longueur nulle. Rien n'interdit d'écrire après : les décodeurs d'image s'arrêtent à `IEND`, mais les outils qui parcourent les signatures voient la suite. C'est ce comportement qui rend la polyglotte possible.

## Solution

### Triage

```bash
exiftool flag.png
strings -n 8 flag.png | grep secret
binwalk flag.png
```

Les trois commandes se recoupent : le warning de trailer, les chemins `secret/` et l'offset `0x9B3B` désignent la même archive.

### Extraction

```bash
binwalk -e flag.png
ls -la _flag.png.extracted/secret/
eog _flag.png.extracted/secret/flag.png
```

`unzip flag.png` fonctionne aussi : le ZIP concaténé est accepté malgré les données PNG qui le précèdent (un avertissement est émis, l'extraction se fait quand même).

### Lecture

Le fichier extrait `secret/flag.png` est une image affichant le flag en clair : il faut l'**ouvrir**, pas la passer à `strings` (le texte est dessiné dans les pixels).

On garde aussi le dossier d'extraction : si la première image ne montre rien, il peut contenir d'autres sorties produites par `binwalk` au même offset.

### Pourquoi ça marche

L'archive n'est pas cachée dans les pixels, elle est ajoutée au conteneur. Le PNG reste valide, et le ZIP l'est aussi parce qu'un décompresseur localise sa table de fin de répertoire central depuis la fin du fichier : les données PNG qui précèdent la première entrée locale ne le gênent pas.

Deux formats, un seul fichier : c'est le principe de la polyglotte.

## Pièges

- **Passer l'image extraite à `strings`** : le flag est dessiné, aucun octet de texte ne le contient.
- **Tronquer le PNG** : un recadrage ou un réenregistrement détruit le trailer ; on travaille sur une copie de l'original.
- **Croire que `unzip` refuse** : il avertit sur les octets parasites mais extrait le contenu ; `binwalk -e` est plus direct.
- **Chercher le flag dans les EXIF** : les métadonnées ne contiennent que le warning de trailer, la valeur est dans l'image imbriquée.
- **Oublier de parcourir tout le fichier** : l'archive commence à `0x9B3B`, pas juste après les données d'image visibles.
- **Utiliser `-e` sans répertoire de travail propre** : `binwalk` extrait dans `_<nom>.extracted/`, un dossier déjà présent peut mélanger les résultats de plusieurs essais.
- **Se fier au seul `binwalk`** : la signature peut être décalée ; le recoupement avec `strings` et `exiftool` confirme l'offset.
- **Réenregistrer l'image depuis un visualiseur** : l'outil réécrit le fichier et perd le trailer, donc l'archive.

## Flag

Flag validé sur la plateforme (valeur non conservée).
