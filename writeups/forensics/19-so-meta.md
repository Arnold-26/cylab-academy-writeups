# 19 — So Meta

**Événement** : picoCTF 2019 · **Catégorie** : Forensics · **Auteur** : Kevin Cooper/Danny

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

Une image `pico_img.png` est fournie avec la consigne « Find the flag in this picture ». Les
indices orientent vers la notion de métadonnées de fichier (« What does meta mean in the context of
files? », « Ever heard of metadata? »).

## Analyse

La démarche forensique standard sur une image est une courte checklist : métadonnées, chaînes
imprimables, fichiers embarqués. Ici, le flag n'est pas dans les pixels mais dans les champs EXIF
du PNG — plus exactement dans le champ `Artist`, un champ libre prévu pour le nom du photographe.

`exiftool` décode la structure EXIF/XMP et affiche un tableau `champ : valeur`, ce qui rend la
valeur immédiatement lisible, contrairement à un `strings` qui noierait le résultat dans le bruit
des chunks PNG ou à une recherche hexadécimale qui ne nommerait pas le champ (tag `0x013B`).

## Solution

1. Installer l'outil si nécessaire : `sudo apt install libimage-exiftool-perl`.
2. Dumper l'ensemble des métadonnées :

```bash
exiftool pico_img.png
```

3. Repérer la ligne utile (le champ `Artist`) :

```
Artist                          : picoCTF{s0_m3ta_43f253bb}
```

4. Variante en filtrant directement :

```bash
exiftool pico_img.png | grep Artist
```

5. Contrôle complémentaire utile en cas de doute : `strings pico_img.png | grep picoCTF` ou
   `binwalk pico_img.png` pour vérifier l'absence d'archive embarquée.

## Flag

`picoCTF{s0_m3ta_43f253bb}`

## Sources

- https://raw.githubusercontent.com/HHousen/PicoCTF-2019/master/Forensics/So%20Meta/README.md — énoncé, commande `exiftool` filtrée et valeur exacte du champ `Artist`
- https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/master/picoCTF_2019/Forensics/So_Meta.md — démarche forensique détaillée et sortie complète d'`exiftool` (champ `Artist`, avertissement sur les chunks texte après `IDAT`)
