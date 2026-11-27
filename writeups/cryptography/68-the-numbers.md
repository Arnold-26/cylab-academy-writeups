# 68 — The Numbers

**Événement** : picoCTF 2019 · **Catégorie** : Cryptography · **Auteur** : Pandu

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

Une image contenant la suite « The numbers... what do they mean? » est fournie : elle affiche des
nombres séparés par des espaces, encadrés d'accolades. L'indice précise que le flag est au format
`PICOCTF{}`.

## Analyse

La présence d'accolades non chiffrées indique une substitution caractère par caractère. Toutes les
valeurs sont comprises entre 1 et 26 : ce sont des positions dans l'alphabet, donc un encodage
A1Z26. La lettre `A` vaut 1, `B` vaut 2, … `Z` vaut 26.

Les nombres lus sur l'image sont :

```
16 9 3 15 3 20 6 { 20 8 5 14 21 13 2 5 18 19 13 1 19 15 14 }
```

Le décodage direct en `A=1` donne `PICOCF{...}` avec des lettres décalées d'un cran si l'on
utilise un indexage à base zéro (`ascii_uppercase[n]` au lieu de `ascii_uppercase[n-1]`). Le piège
classique est là : Python indexe les chaînes à partir de 0, l'alphabet A1Z26 à partir de 1.

## Solution

1. Relever la suite de nombres dans l'image (lecture visuelle ou OCR).
2. Décoder avec un script, en corrigeant l'index :

```python
import string
ALPHABET = string.ascii_uppercase
enc = "16 9 3 15 3 20 6 { 20 8 5 14 21 13 2 5 18 19 13 1 19 15 14 }".split()
flag = ""
for num in enc:
    flag += ALPHABET[int(num) - 1] if num.isnumeric() else num
print(flag)
# PICOCTF{THENUMBERSMASON}
```

3. Variante sans script : CyberChef avec l'opération `Magic` sur la partie numérique, ou un
   décodeur A1Z26 en ligne, en ajoutant manuellement les accolades (ces outils ignorent les
   caractères non numériques).
4. Soumettre le résultat tel quel, en respectant la casse donnée par l'énoncé.

## Flag

`PICOCTF{THENUMBERSMASON}`

## Sources

- https://raw.githubusercontent.com/ir0nstone/cybersec-notes/refs/heads/master/writeups/picogym/cryptography/the-numbers.md — relevé des nombres, script de décodage, explication du décalage d'indice et résultat
- https://raw.githubusercontent.com/Ne0Lux-C1Ph3r/WRITE-UP/master/picoCTF2019/Cryptography/index.md — énoncé d'origine, mention de l'encodage alphabétique et flag au format majuscule
