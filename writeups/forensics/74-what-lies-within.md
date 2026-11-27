# 74 — What Lies Within

**Événement** : picoCTF 2019 · **Catégorie** : Forensics · **Auteur** : Julio/Danny

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

Une image `buildings.png` est fournie avec la phrase « There's something in the building. Can you
retrieve the flag? ». L'indice signale que des données sont encodées quelque part et qu'un décodeur
en ligne peut suffire.

## Analyse

Il s'agit de stéganographie LSB : les bits de poids faible des canaux de couleur des pixels sont
utilisés pour transporter un message, invisible à l'œil car modifier le dernier bit d'un octet de
couleur change la teinte de façon imperceptible.

Sur un PNG (compression sans perte), les outils de référence sont `zsteg` et `stegsolve`. Sur un
JPEG, il faudrait `steghide` ou `outguess`, la compression avec perte détruisant le LSB. `zsteg`
teste systématiquement les combinaisons canal / ordre de bits / disposition et affiche le texte
extrait pour chaque variante : la ligne utile est celle dont le texte est lisible.

## Solution

1. Vérifier le type et les métadonnées du fichier, par acquit de conscience :

```bash
file buildings.png
exiftool buildings.png
```

2. Lancer l'extraction LSB :

```bash
zsteg buildings.png
```

3. Repérer la ligne dont le texte est le flag :

```
b1,rgb,lsb,xy       .. text: "picoCTF{h1d1ng_1n_th3_b1t5}"
```

4. Variante sans outil local : un décodeur de stéganographie en ligne (stylesuxx) donne le même
   résultat en important l'image.
5. Contrôle complémentaire possible : `zsteg -a buildings.png` pour tester toutes les
   combinaisons, ou `binwalk` pour vérifier l'absence de donnée ajoutée en fin de fichier.

## Flag

`picoCTF{h1d1ng_1n_th3_b1t5}`

## Sources

- https://raw.githubusercontent.com/HHousen/PicoCTF-2019/master/Forensics/What%20Lies%20Within/README.md — énoncé, sortie complète de `zsteg` et flag extrait
- https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/master/picoCTF_2019/Forensics/What_Lies_Within.md — rappel PNG/JPEG sur le choix de l'outil (zsteg vs steghide) et alternative en ligne
