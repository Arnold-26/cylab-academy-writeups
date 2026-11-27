# Pitter, Patter, Platters

**Catégorie** : Forensics · **Challenge** : #87 · **Résolu le** : 2026-11-25

## Énoncé

> suspicious.dd.sda1 (32 Mo, ext3)

## Résolution

Méthode : **flag dans le slack space, encode UTF-16LE et inverse**.

Image disque ext3 (Tiny Core Linux, 32 Mo). `fls -r -p` montre un fichier **`suspicious-file.txt`** a la racine (inode 12) qui ne contient que « Nothing to see here! But you may want to look here --> ». C'est un leurre qui pointe en fait vers le **slack space** : le fichier fait 55 octets mais occupe un bloc de 1024 (`istat` donne le bloc direct **2049**). En lisant le bloc entier a l'offset `2049*1024` et en prenant les octets apres le 55e, on trouve une chaine **UTF-16LE inversee** (`}` puis `e\x00` puis `1\x00` ...). Decodee puis retournee, elle donne `academy{b3_5t111_mL|_<3_d18a1e1e}`. Pieges : le decodage UTF-16 sur une longueur impaire produit un caractere de remplacement en tete apres inversion (il faut tronquer a un nombre pair d'octets), et le fichier leurre ne contient pas le flag — seul le slack le porte.

## Flag

```
academy{b3_5t111_mL|_<3_d18a1e1e}
```

## Ce qu'il faut retenir

—

## Scripts

- [`solve.py`](../../solve/87/solve.py)
- *7 variantes intermediaires dans `solve/87/archive/`*
