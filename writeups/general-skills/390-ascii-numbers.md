# 390 — ASCII Numbers

**Événement** : picoGym / Challenge Library Exclusive · **Catégorie** : General Skills · **Auteur** : LT « syreal » Jones

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

« Convertissez la chaîne de nombres ASCII suivante en une chaîne lisible : »

```
0x70 0x69 0x63 0x6f 0x43 0x54 0x46 0x7b 0x34 0x35 0x63 0x31 0x31 0x5f 0x6e 0x30 0x5f
0x71 0x75 0x33 0x35 0x37 0x31 0x30 0x6e 0x35 0x5f 0x31 0x6c 0x6c 0x5f 0x74 0x33 0x31
0x31 0x5f 0x79 0x33 0x5f 0x6e 0x30 0x5f 0x6c 0x31 0x33 0x35 0x5f 0x34 0x34 0x35 0x64
0x34 0x31 0x38 0x30 0x7d
```

Indices : CyberChef est l'outil idéal pour tout encodage, en particulier ASCII ; essayer la
recette « From Hex ».

## Analyse

Aucune cryptographie : chaque token est un octet écrit en hexadécimal, précédé de `0x`. La
seule subtilité est de ne pas se contenter de remplacer les `0x` — il faut **réellement
convertir** 2 chiffres hexadécimaux en un caractère (par exemple `0x70` → `p`, et non `70`).

La chaîne commence par `0x70 0x69 0x63 0x6f 0x43 0x54 0x46 0x7b` = `picoCTF{` et finit par
`0x7d` = `}` : la structure du flag est immédiatement reconnaissable, ce qui valide
l'hypothèse avant même la fin du décodage.

## Solution

**CyberChef** (le plus rapide) : coller la chaîne dans *Input*, ajouter la recette
**From Hex** avec `Auto` comme délimiteur → la sortie est le flag.

**Python** (reproductible, sans dépendance réseau) :

```python
enc = "0x70 0x69 0x63 0x6f 0x43 0x54 0x46 0x7b ... 0x7d".split()
print(''.join(map(chr, map(lambda x: int(x, 16), enc))))
```

**Shell** :

```bash
echo "70 69 63 6f 43 54 46 7b ... 7d" | xxd -r -p
```

Les trois donnent la même chaîne : `picoCTF{...1ll_t311_y3_n0_l135...}` — le texte est du
leet speak, pas une donnée chiffrée.

## Flag

```
picoCTF{45c11_n0_qu35710n5_1ll_t311_y3_n0_l135_445d4180}
```

## Sources

- https://github.com/Cajac/picoCTF-Writeups/blob/main/Challenge_Library_Exclusive/General_Skills/ASCII_Numbers.md
- https://gchq.github.io/CyberChef/
- https://qiita.com/colza_/items/2870f65de88589721b08
