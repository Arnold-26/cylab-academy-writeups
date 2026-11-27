# Binary Digits

**Catégorie** : Forensics · **Challenge** : #698

## Résolution

`digits.bin` = la représentation binaire d'un JPEG. Regroupement par 8 bits → JPEG reconstruit → l'image affiche le flag.

## Flag

```
academy{h1dd3n_1n_th3_b1n4ry_1b150ee9}
```

## Ce qu'il faut retenir

Un fichier de 0/1 se reconstruit : 8 bits = 1 octet, puis `file` pour reconnaître le format.
