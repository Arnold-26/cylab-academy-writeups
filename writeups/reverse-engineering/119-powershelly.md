# Powershelly

**Catégorie** : Reverse Engineering · **Challenge** : #119 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **inversion d'une permutation + chaine XOR PowerShell**.

Le script PowerShell lit `input.txt` (9245 octets = **5 lignes** de 264 champs de 6 bits, ce qui colle exactement a `$numLength = 264*30 + 265*5`), empile les 5 lignes par colonne (`$blocks[$j]` = les 5 morceaux de 6 bits de la colonne j, soit 30 bits), puis : `Scramble(bloc, seed)` construit 30 emplacements a `"10"`, et pour i=0..29 ecrit `"11"` ou `"00"` au premier emplacement libre en partant de `(i*seed) % 30` (une **permutation**, donc inversible) ; la sortie enchainee est `result_i = fun_i XOR result_{i-1} XOR randoms_i`. On recupere donc `fun_i = result_i XOR result_{i-1} XOR randoms_i` avec `randoms[i] = ((i+1)*327 % 681 + 344) % 313`, on verifie que chaque fun (60 bits) ne contient que des paires 11/00 (0 non conforme -> validation), puis on inverse la permutation avec `seeds[i] = ((i+1)*127) % 500`. Les 30 lignes resultantes se lisent en ASCII : `academy{2018highw@y_2_pow3r$hel!}` (les lignes en 0x9e.. sont la meme chaine XOR 0xff).

## Flag

```
academy{2018highw@y_2_pow3r$hel!}
```

## Ce qu'il faut retenir

—
