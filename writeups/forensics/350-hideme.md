# 350 — hideme

**Événement** : picoCTF 2023 · **Catégorie** : Forensics · **Auteur** : Geoffrey Njogu

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

« Chaque fichier obtient un flag. L'analyste SOC a vu une image être envoyée et renvoyée entre
deux personnes. En l'examinant, il s'est rendu compte qu'il y avait plus que ce que l'œil
perçoit. »

## Analyse

Le fichier est un PNG (`flag.png`, 512×504, RGBA). Trois vérifications réflexes :

1. **Métadonnées** — `exiftool` signale `Warning: [minor] Trailer data after PNG IEND chunk` :
   il y a des données après la fin officielle du PNG.
2. **Chaînes** — `strings -n 8` fait apparaître des chemins `secret/` et `secret/flag.png`,
   signature d'une archive ZIP concaténée.
3. **Signatures** — `binwalk` confirme une archive ZIP à l'offset `0x9B3B`, contenant deux
   entrées : le dossier `secret/` et `secret/flag.png`.

Technique : « fichier dans le fichier » (polyglotte PNG+ZIP). Le décodeur PNG ignore tout ce
qui suit le chunk `IEND`, tandis qu'un décompresseur ZIP trouve son en-tête `PK\x03\x04` à
l'offset indiqué par sa propre table centrale.

## Solution

```bash
exiftool flag.png
strings -n 8 flag.png | grep secret
binwalk flag.png
binwalk -e flag.png          # ou : unzip flag.png (ZIP concaténé accepté)
ls -la _flag.png.extracted/secret/
eog _flag.png.extracted/secret/flag.png
```

Le fichier extrait `secret/flag.png` est une image affichant le flag en clair : il faut donc
l'**ouvrir**, pas la passer à `strings` (le texte est dessiné dans les pixels).

## Flag

La valeur est à lire dans `secret/flag.png`. Les writeups publics donnent la même phrase mais
avec des suffixes différents selon la capture (`@n_ima9e_85e04ab8`, `@n_ima9e_8210824`,
`...678a337`) : la partie stable est `picoCTF{Hiddinng_An_imag3_within_@n_ima9e_...}`. La
seule valeur fiable est celle affichée par l'extraction locale.

```
picoCTF{Hiddinng_An_imag3_within_@n_ima9e_85e04ab8}
```

## Sources

- https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2023/Forensics/hideme.md
- https://mileshandelman.com/writeups/hideme/
- https://github.com/noamgariani11/picoCTF-2023-Writeup/blob/main/Forensics/hideme/hideme.md
