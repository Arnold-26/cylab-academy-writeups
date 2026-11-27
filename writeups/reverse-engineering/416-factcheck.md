# FactCheck

**Catégorie** : Reverse Engineering · **Challenge** : #416 · **Résolu le** : 2026-11-23

## Énoncé

> This binary is putting together some important piece of information... Can you uncover that information?
>
> Examine this [file](https://challenge-files.cylabacademy.net/library/e4fca72f5291fff942a3454ae5c143bd0d23ea12eeb4466db379053a770a4fe1/bin). Do you understand its inner workings?

## Résolution

Méthode : **evaluation statique des append conditionnels**.

Le binaire C++ construit le flag par une serie de `std::string::operator+=`, dont certains sont conditionnels (comparaisons sur le premier caractère de variables intermediaires). En evaluant chaque condition (`'5'<='A'` vrai, `'6'!='A'` vrai, `'3'-'e'==3` faux, `'a'=='G'` faux), on obtient la chaîne finale.

## Flag

```
academy{wELF_d0N3_mate_194ca125}
```
