# 52 — extensions

**Événement** : picoCTF 2019 · **Catégorie** : Forensics · **Auteur** : Sanjay C/Danny

## Énoncé

Un fichier nommé `flag.txt` est fourni avec la remarque « This is a really weird text file TXT? ».
Les indices demandent comment un système d'exploitation reconnaît un type de fichier et rappellent
que la réponse n'est pas seulement l'extension.

## Analyse

L'extension `.txt` est une convention de nommage : elle n'est inscrite nulle part dans le contenu du
fichier. Les systèmes d'exploitation, et surtout les outils d'analyse, s'appuient sur les **nombres
magiques** en tête de fichier — la signature — pour déterminer le type réel.

Un `flag.txt` qui commence par `\x89PNG\r\n\x1a\n` est un PNG, quel que soit son nom. Le premier
réflexe est donc de ne pas ouvrir le fichier par son extension mais de l'identifier :

```bash
file flag.txt
```

`file` lit les signatures dans sa base de données magique et compare les premiers octets. Une fois
le type réel connu, on corrige l'extension : le fichier s'ouvre alors dans une visionneuse d'images,
et le flag est visible dans l'image, le texte étant rendu dans les pixels.

Ce n'est pas de la stéganographie : les données sont l'image elle-même, affichées normalement. Le
seul obstacle est le nom du fichier.

## Solution

1. Identifier le type réel :

```bash
file flag.txt
# flag.txt: PNG image data, 1697 x 608, 8-bit/color RGB, non-interlaced
```

2. Vérifier la signature en hexadécimal, pour ne pas dépendre d'un seul outil :

```bash
xxd flag.txt | head -2
# 00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
```

`89 50 4E 47 0D 0A 1A 0A` est la signature PNG ; `49 48 44 52` (`IHDR`) confirme le premier chunk.

3. Renommer le fichier avec la bonne extension :

```bash
mv flag.txt flag.png
```

4. Ouvrir l'image dans une visionneuse et lire le flag :

```bash
eog flag.png          # ou feh, xdg-open, display
```

5. Variante sans interface graphique, utile en session distante : OCR de l'image.

```bash
tesseract flag.png - | grep -i -E 'ctf|flag'
```

6. Contrôle d'intégrité, pour vérifier que le fichier n'a pas été altéré par le transfert :

```bash
pngcheck -v flag.png
```

## Pièges

- **`file` sur un fichier tronqué.** Un transfert interrompu donne `data` au lieu de `PNG image
  data` : on re-télécharge avant de conclure.
- **Se fier à la visionneuse du système.** Un gestionnaire de fichiers peut refuser d'ouvrir un
  `.txt` comme une image, ou afficher du binaire. Le renommage est nécessaire, pas facultatif.
- **OCR bruité.** `tesseract` sur une capture d'écran de flag peut confondre `l`, `1` et `I` : la
  lecture visuelle reste la référence, l'OCR servant au dégrossissage.
- **Confondre avec de la stéganographie.** Ici le flag est le contenu visible de l'image ; lancer
  `zsteg` ou `steghide` serait une fausse piste.

**Pourquoi ça marche.** L'extension n'est qu'un indicateur pour l'utilisateur ; le chargeur d'image,
lui, lit les octets magiques. Renommer ne modifie pas le contenu, seulement la façon dont les outils
l'interprètent. La leçon vaut pour tous les formats : c'est la signature qui fait foi, et `file` est
l'outil qui la lit.
