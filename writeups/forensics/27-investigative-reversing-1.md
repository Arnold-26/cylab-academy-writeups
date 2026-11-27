# Investigative Reversing 1

**Catégorie** : Forensics · **Challenge** : #27 · **Résolu le** : 2026-11-25

## Énoncé

> A binary and three images.

## Résolution

Méthode : **multi-artifact split**.

Meme schema que IR0 (append en fin de PNG) mais le flag est **decoupe entre trois
images**, et l'ordre d'ecriture est melange. Le desassemblage de `main` donne exactement :

| image | octets ecrits |
|---|---|
| `mystery.png` (fichier 1) | `flag[4]`, `flag[6..9]`, `flag[15..25]` |
| `mystery2.png` | `flag[0]+21`, une constante |
| `mystery3.png` | `flag[1]`, `flag[2]`, `flag[5]`, `flag[10..14]` |

Donnees effectivement trouvees apres le chunk `IEND` :

```
mystery.png  -> ey{An1_1730fa2f   (16 o)
mystery2.png -> vh                (2 o)
mystery3.png -> cam0tha_          (8 o)
```

On verifie la coherence : `flag[0]+21 = 'a'+21 = 'v'` ; `flag[1]='c'`, `flag[2]='a'`,
`flag[5]='m'`, `flag[7]='{'` — tout colle avec le prefixe `academy{`. L'index 3 n'est ecrit
nulle part : c'est le `d` de `academy`, deduit du format.

Reconstruction : `academy{An0tha_1_1730fa2f}`.

**Lecon** : quand un flag est decoupe en plusieurs artefacts, ecrire le tableau
« indice -> fichier » avant de concatener. Ici l'ordre alphabetique des fichiers donne
`cam0tha_vhey{...}` qui ne ressemble a rien.

## Flag

```
academy{An0tha_1_1730fa2f}
```

## Ce qu'il faut retenir

—
