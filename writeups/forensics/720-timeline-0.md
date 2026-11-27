# 720 — Timeline 0

**Événement** : picoCTF 2026 · **Catégorie** : Forensics

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« Can you find the flag in this disk image? Wrap what you find in the picoCTF flag format. »
L'image fournie est `partition4.img.gz`.

## Analyse
Le nom du challenge annonce la couleur : le flag est caché derrière des **horodatages manipulés**.
Après décompression, on construit une chronologie MAC complète avec les outils The Sleuth Kit, puis
on cherche l'anomalie.

La timeline commence en 2021 : une entrée datée de **janvier 1985** est impossible (bien antérieure
à la création du système de fichiers). C'est du *timestomping*. Le fichier repéré est `/bin/bcab`,
inode **4945**. On lit son contenu par inode avec `icat` (indépendant de l'entrée de répertoire),
puis on constate que le contenu est de l'alphanumérique terminé par un retour à la ligne : du
base64. Le décodage donne le corps du flag, à envelopper dans `picoCTF{}`.

## Solution
```bash
gunzip partition4.img.gz
fls -m '/' -r partition4.img > body.txt
mactime -b body.txt > timeline.txt
grep '1985' timeline.txt          # /bin/bcab, inode 4945
icat partition4.img 4945 > bcab
cat bcab
base64 -d bcab
```
L'intérêt du bodyfile `fls -m` est de produire une ligne par entrée avec inode, chemin et les quatre
horodatages : le tri chronologique fait ressortir immédiatement la date aberrante, et l'inode sert
ensuite à extraire le contenu.

## Flag
```
picoCTF{71m311n3_0u7113r_h3r_43a2e7af}
```

## Sources
- https://picoctfsolutions.com/picoctf-2026-timeline-0 — page de solution picoCTF 2026 (bodyfile, mactime, inode 4945, `icat`)
- https://qiita.com/0xyu/items/22808f2a8931a27724e2 — writeup picoCTF 2026 « Timeline 0 » (flag complet)
