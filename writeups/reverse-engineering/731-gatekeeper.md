# 731 — Gatekeeper

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« What's behind the numeric gate? You only get access if you enter the right kind of number. »
Le binaire `gatekeeper` est fourni : il faut inverser ses contrôles numériques et fournir la valeur
qui passe.

## Analyse
Le binaire demande un nombre et applique **deux contrôles indépendants** :
1. une contrainte de **longueur** sur la chaîne saisie (3 caractères) ;
2. un contrôle de **valeur** sur l'entier obtenu après conversion, qui doit être supérieur à 999.

Aucun entier décimal de 3 caractères ne dépasse 999 : la conversion ne peut donc être décimale. Le
binaire utilise `strtol`, qui accepte le préfixe/format hexadécimal : `3e8` (hexadécimal de 1000)
satisfait les deux contrôles à la fois.

Une fois le « portail » franchi, `reveal_flag` n'imprime pas le flag directement : il l'affiche à
l'envers en insérant la chaîne `picoCTF_` tous les 4 caractères. Il faut donc retirer ces
occurrences, puis inverser le reste.

## Solution
```bash
chmod +x gatekeeper
./gatekeeper
echo '3e8' | ./gatekeeper
# retirer les insertions puis inverser
echo '<sortie>' | sed -e 's/picoCTF_//g' | rev
# équivalent Python
python3 -c "o='<sortie>'; print(o.replace('picoCTF_','')[::-1])"
```

## Flag
```
flag non conservé
```
La page de solution publique ne montre que le début du flag, sous la forme
`picoCTF{3_digit_hex_GT_999_...}` : la valeur complète n'est pas publiée.

## Sources
- https://picoctfsolutions.com/picoctf-2026-gatekeeper — page de solution picoCTF 2026 (double contrôle longueur/valeur, `3e8`, `reveal_flag` inversé)
