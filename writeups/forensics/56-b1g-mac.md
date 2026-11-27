# B1g_Mac

**Catégorie** : Forensics · **Challenge** : #56 · **Résolu le** : 2026-11-24

## Énoncé

> https://challenge-files.cylabacademy.net/library/.../b1g_mac.zip

## Résolution

Méthode : **flag cachee dans les bits faibles des timestamps NTFS des champs extra ZIP**.

L'archive contient `main.exe` (PE32 inutile ici, il lit un flag.txt absent du depot) et `test/` avec 9 BMP et leurs 9 copies « - Copy ». Les BMP sont des **doublons stricts** (md5 identiques) : le contenu ne porte rien. Le nom du challenge est un jeu de mots sur **MAC = Modification, Access, Creation**, les trois timestamps NTFS. Chaque entree du ZIP possede un extra field id `0x000a` (NTFS) contenant le tag `0x0001` et trois FILETIME 64 bits (M, A, C). Les fichiers originaux ont des valeurs « propres » finissant par 000000, alors que les copies ont leurs bits faibles modifies : en prenant les **16 bits de poids faible du timestamp de Modification**, en big-endian, dans l'ordre alphabetique des 9 copies, on obtient exactement `academy{M4cTim35!}`. Les timestamps A et C donnent du bruit, ce qui confirme que seul M est utilise. Aucun outil de steganographie n'etait necessaire : tout se lit dans les metadonnees du ZIP avec le module `zipfile` de Python.

## Flag

```
academy{M4cTim35!}
```

## Scripts

- [`solve.py`](../../solve/56/solve.py)
- *9 variantes intermediaires dans `solve/56/archive/`*
