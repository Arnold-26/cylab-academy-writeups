# 19 — So Meta

**Événement** : picoCTF 2019 · **Catégorie** : Forensics · **Auteur** : Kevin Cooper/Danny

## Énoncé

Une image `pico_img.png` est fournie avec la consigne « Find the flag in this picture ». Les indices
orientent vers la notion de métadonnées de fichier (« What does meta mean in the context of
files? », « Ever heard of metadata? »).

## Analyse

Sur une image, la démarche forensique tient en une courte checklist : type réel, métadonnées,
chaînes imprimables, fichiers embarqués. On la déroule dans cet ordre, du moins coûteux au plus
coûteux.

```bash
file pico_img.png
# PNG image data, 640 x 480, 8-bit/color RGB, non-interlaced
```

Le fichier est bien un PNG. Le flag n'est pas dans les pixels mais dans les champs EXIF du fichier —
plus exactement dans le champ `Artist`, un champ libre prévu à l'origine pour le nom du photographe.
C'est un emplacement classique : les métadonnées traversent les retouches, les conversions et les
copies sans être réinitialisées.

L'outil `exiftool` décode la structure EXIF/XMP et affiche un tableau `champ : valeur`, ce qui rend
la valeur immédiatement lisible. Un `strings` noierait le résultat dans le bruit des chunks PNG, et
une recherche hexadécimale ne nommerait pas le champ : `Artist` correspond au tag EXIF `0x013B`
(`0x13B` en décimal 315), ce qui reste utile à savoir si l'on veut extraire la valeur à la main.

## Solution

1. Installer l'outil si nécessaire :

```bash
sudo apt install libimage-exiftool-perl
```

2. Dumper l'ensemble des métadonnées :

```bash
exiftool pico_img.png
```

3. Repérer la ligne utile, le champ `Artist` :

```
Artist                          : <flag>
```

4. Filtrer directement, ce qui évite de parcourir tout le tableau :

```bash
exiftool pico_img.png | grep Artist
```

5. Extraction ciblée du tag, si l'on veut se passer du nom du champ :

```bash
exiftool -Artist pico_img.png
exiftool -b -Artist pico_img.png        # valeur brute, sans le nom du champ
```

6. Contrôles complémentaires, utiles en cas de doute sur la nature du fichier :

```bash
strings pico_img.png | grep -i -E 'flag|ctf'
binwalk pico_img.png                     # archive ou fichier ajouté en fin de fichier
pngcheck -v pico_img.png                 # cohérence des chunks
```

## Pièges

- **Lire les pixels.** Aucune stéganographie ici : une analyse LSB (`zsteg`) ne donnerait rien, et
  le flag est en clair dans l'en-tête.
- **`exiftool` sur une copie renommée.** Les métadonnées survivent au renommage, mais pas toujours
  à un passage par un éditeur d'image, qui peut les réécrire. On travaille sur le fichier d'origine.
- **Champ `Artist` vide dans certains lecteurs.** Les visionneuses grand public masquent les champs
  EXIF non standard ; il faut l'outil en ligne de commande.
- **Chunk texte après `IDAT`.** Un PNG peut aussi porter des chunks `tEXt`/`zTXt` ; `exiftool` les
  affiche, mais un chunk ajouté après les données de l'image est un signe de concaténation, à
  vérifier avec `binwalk` ou `pngcheck`.

**Pourquoi ça marche.** Les métadonnées sont des données annexes, stockées en clair dans le fichier
et transportées telles quelles. Rien ne les efface par défaut : une chaîne ajoutée dans le champ
`Artist` reste lisible par toute personne qui sait regarder l'en-tête plutôt que l'image.
