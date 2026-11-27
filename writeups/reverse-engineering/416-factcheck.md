# FactCheck

**Catégorie** : Reverse Engineering · **Challenge** : #416 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **evaluation statique des append conditionnels**.

Le binaire C++ construit le flag par une serie de `std::string::operator+=`, dont certains sont conditionnels (comparaisons sur le premier caractere de variables intermediaires). En evaluant chaque condition (`'5'<='A'` vrai, `'6'!='A'` vrai, `'3'-'e'==3` faux, `'a'=='G'` faux), on obtient la chaine finale.

## Flag

```
academy{wELF_d0N3_mate_194ca125}
```
