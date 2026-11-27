# 68 — The Numbers

**Événement** : picoCTF 2019 · **Catégorie** : Cryptography · **Auteur** : Pandu

## Énoncé

Une image contenant la suite « The numbers... what do they mean? » est fournie : elle affiche des
nombres séparés par des espaces, encadrés d'accolades. L'indice précise que le flag est au format
habituel, en majuscules et accolades comprises.

## Analyse

La présence d'accolades non chiffrées indique une substitution caractère par caractère : la
ponctuation structurelle est restée en clair, seules les lettres ont été remplacées. Toutes les
valeurs sont comprises entre 1 et 26, ce qui les désigne immédiatement comme des positions dans
l'alphabet — un encodage A1Z26, où `A` vaut 1, `B` vaut 2, … `Z` vaut 26.

Les nombres lus sur l'image sont :

```
16 9 3 15 3 20 6 { 20 8 5 14 21 13 2 5 18 19 13 1 19 15 14 }
```

Le décodage est une simple projection sur l'alphabet. Le piège classique est l'**indice de base** :
Python indexe les chaînes à partir de 0, l'alphabet A1Z26 à partir de 1. Utiliser directement
`ascii_uppercase[n]` décale toutes les lettres d'un cran et produit une suite incohérente du type
`PICOCF`, ce qui met sur la piste sans donner le bon résultat. Il faut écrire `ascii_uppercase[n-1]`.

Le résultat est en majuscules, conformément au format annoncé par l'énoncé ; la casse fait partie de
la réponse à soumettre.

## Solution

1. Relever la suite de nombres dans l'image, à la lecture visuelle ou par OCR :

```bash
tesseract numbers.png - 2>/dev/null
```

2. Décoder avec un script, en corrigeant l'indice :

```python
import string

ALPHABET = string.ascii_uppercase
enc = "16 9 3 15 3 20 6 { 20 8 5 14 21 13 2 5 18 19 13 1 19 15 14 }".split()

flag = ""
for num in enc:
    flag += ALPHABET[int(num) - 1] if num.isnumeric() else num

print(flag)
```

3. Variante compacte, sans boucle :

```python
print(''.join(chr(int(n) + 64) if n.isdigit() else n for n in enc))
```

`chr(1 + 64)` vaut `A` : c'est le même décalage, exprimé autrement.

4. Contrôle de cohérence avant de soumettre : la longueur doit correspondre au nombre de symboles
   lus, et les accolades doivent se trouver aux extrémités. Une lettre fausse au milieu signale une
   erreur de lecture de l'image, pas de décodage.

5. Soumettre le résultat tel quel, en respectant la casse donnée par l'énoncé.

## Pièges

- **Indice à base zéro.** `ALPHABET[int(num)]` au lieu de `ALPHABET[int(num) - 1]` décale tout d'une
  lettre. C'est l'erreur la plus fréquente sur A1Z26, et elle produit un texte qui *ressemble* à des
  mots, ce qui la rend difficile à repérer.
- **Confondre A1Z26 et A0Z25.** Un encodage qui commence à 0 contient des `0` ; ici les valeurs vont
  de 1 à 26, sans zéro.
- **OCR approximatif.** Sur une image de mauvaise qualité, `1` est lu `l` ou `7` : le relevé doit
  être vérifié à l'œil avant d'être soumis.
- **Casse.** Le format imposé est en majuscules ; un flag reconstitué en minuscules est refusé par
  la plateforme alors que le décodage est juste.
- **Accolades.** Les décodeurs en ligne ignorent les caractères non numériques : ils rendent les
  lettres mais pas les accolades, qu'il faut replacer à la main.

**Pourquoi ça marche.** A1Z26 est une substitution monoalphabétique sans clé : la position d'une
lettre dans l'alphabet est une information publique. La structure du flag (accolades, longueur)
révèle immédiatement la nature du codage, et le décodage se fait en une ligne. Aucune cryptanalyse
n'est nécessaire, seulement l'attention au décalage d'indice.

## Flag

Flag validé sur la plateforme (valeur non conservée).
