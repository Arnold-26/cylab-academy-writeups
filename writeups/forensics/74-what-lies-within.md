# 74 — What Lies Within

**Événement** : picoCTF 2019 · **Catégorie** : Forensics · **Auteur** : Julio/Danny

## Énoncé

Une image `buildings.png` est fournie avec la phrase « There's something in the building. Can you
retrieve the flag? ». L'indice signale que des données sont encodées quelque part et qu'un décodeur
peut suffire.

## Analyse

Le fichier est un PNG, donc une compression **sans perte** : chaque octet de couleur est restitué
exactement tel qu'il a été écrit. C'est la condition qui rend la stéganographie LSB possible.

Le principe : les bits de poids faible des canaux de couleur des pixels sont utilisés pour
transporter un message. Modifier le dernier bit d'un octet de couleur change la teinte de 1/255,
imperceptible à l'œil, mais le bit est bien là — et il est lisible par quiconque sait où regarder.
Un message ASCII de 32 caractères tient dans 256 bits, soit 256 octets de couleur, une fraction
infime d'une image de quelques centaines de kilooctets.

Le choix de l'outil dépend du format :

- sur un **PNG**, les outils de référence sont `zsteg` et `stegsolve`, car le LSB survit à la
  compression sans perte ;
- sur un **JPEG**, il faudrait `steghide` ou `outguess`, la compression avec perte détruisant le LSB
  lors de la réécriture.

`zsteg` teste systématiquement les combinaisons canal / ordre de bits / disposition et affiche le
texte extrait pour chaque variante : la ligne utile est celle dont le texte est lisible. C'est plus
rapide que d'écrire un extracteur soi-même, et cela couvre les variantes auxquelles on ne penserait
pas.

## Solution

1. Vérifier le type et les métadonnées, par acquit de conscience :

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
b1,rgb,lsb,xy       .. text: "<flag>"
```

La notation se lit ainsi : `b1` = 1 bit par canal, `rgb` = les trois canaux de couleur, `lsb` = bit
de poids faible, `xy` = parcours des pixels ligne par ligne.

4. Extraction ciblée de la variante utile, pour éviter de noyer le résultat :

```bash
zsteg -E 'b1,rgb,lsb,xy' buildings.png | head -c 200
```

5. Variante sans outil local : un décodeur de stéganographie en ligne donne le même résultat en
   important l'image. L'important est de choisir le mode « LSB, RGB, ordre des pixels » et non un
   mode séquentiel sur un seul canal.

6. Contrôles complémentaires :

```bash
zsteg -a buildings.png      # toutes les combinaisons
binwalk buildings.png       # donnée ajoutée en fin de fichier
pngcheck -v buildings.png   # cohérence des chunks
```

## Pièges

- **Mode d'extraction.** `zsteg` sans option essaie les variantes les plus courantes, mais certaines
  images n'utilisent qu'un canal (rouge seul) ou un ordre de bits différent. `-a` explore tout, au
  prix de beaucoup de bruit.
- **Traiter un JPEG comme un PNG.** Le LSB d'un JPEG est écrasé par la recompression : chercher un
  LSB sur un JPEG ne donne que du bruit, il faut `steghide` (avec ou sans phrase de passe).
- **Texte tronqué.** Les premiers caractères peuvent être illisibles (en-tête de longueur) ; on
  cherche le motif du flag dans la sortie brute plutôt que de conclure à l'absence.
- **Lecture à l'œil.** Le flag peut être rendu visible par un simple réhaussement de contraste
  (`convert buildings.png -level 0%,10% out.png`) ; c'est un contrôle rapide avant l'extraction.
- **Faux positifs.** `zsteg -a` affiche des dizaines de lignes ; seule une chaîne complète et
  cohérente compte.

**Pourquoi ça marche.** Le LSB est le bit le moins significatif d'un octet de couleur : le changer
modifie la valeur de 1 sur 256, en dessous du seuil de perception. Sur un format sans perte, la
valeur est préservée à l'identique jusqu'au décodeur, qui peut donc la relire. La stéganographie ne
chiffre pas le message, elle le cache : un outil qui essaie les combinaisons systématiques le
retrouve.
