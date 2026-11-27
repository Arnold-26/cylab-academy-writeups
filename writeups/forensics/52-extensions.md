# 52 — extensions

**Événement** : picoCTF 2019 · **Catégorie** : Forensics · **Auteur** : Sanjay C/Danny

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

Un fichier nommé `flag.txt` est fourni avec la remarque « This is a really weird text file TXT? ».
Les indices demandent comment un système d'exploitation reconnaît un type de fichier et rappellent
que la réponse n'est pas seulement l'extension.

## Analyse

L'extension `.txt` est une simple convention de nommage : elle n'est pas inscrite dans le contenu.
Les systèmes d'exploitation et les outils s'appuient sur les nombres magiques en tête de fichier
(signature). Un `flag.txt` qui commence par `\x89PNG\r\n\x1a\n` est un PNG, quel que soit son nom.

L'outil `file` lit ces signatures pour identifier le type réel. Une fois l'extension corrigée, le
fichier s'ouvre dans une visionneuse d'images et le flag est visible dans l'image (le texte est
rendu dans les pixels).

## Solution

1. Identifier le type réel du fichier :

```bash
file flag.txt
# flag.txt: PNG image data, 1697 x 608, 8-bit/color RGB, non-interlaced
```

2. Vérifier la signature en hexadécimal si nécessaire :

```bash
xxd flag.txt | head -2
```

3. Renommer le fichier avec la bonne extension :

```bash
mv flag.txt flag.png
```

4. Ouvrir l'image (`eog flag.png`, `feh flag.png`, ou n'importe quelle visionneuse) et lire le flag.

5. Variante automatisable sans interface graphique : OCR de l'image, par exemple
   `tesseract flag.png - | grep picoCTF`.

## Flag

`picoCTF{now_you_know_about_extensions}`

## Sources

- https://raw.githubusercontent.com/HHousen/PicoCTF-2019/master/Forensics/extensions/README.md — énoncé, sortie de `file`, procédure de renommage et flag extrait par OCR
- https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/master/picoCTF_2019/Forensics/extensions.md — rappel sur les signatures de fichiers et la sortie exacte de `file`
