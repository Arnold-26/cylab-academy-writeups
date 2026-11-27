# Powershelly

**Catégorie** : Reverse Engineering · **Challenge** : #119 · **Résolu le** : 2026-11-24

## Énoncé

> It's not a bad idea to learn to read Powershell. We give you the output, but do you think you can find the input?
> [rev_PS.ps1](https://challenge-files.cylabacademy.net/library/938553779e78784855f3bf62b3fa104d589bdf501a910a5cd668ffcccffd1fc8/rev_PS.ps1) [output.txt](https://challenge-files.cylabacademy.net/library/938553779e78784855f3bf62b3fa104d589bdf501a910a5cd668ffcccffd1fc8/output.txt)

## Résolution

Méthode : **inversion d'une permutation + chaîne XOR PowerShell**.

Le script PowerShell lit `input.txt` (9245 octets = **5 lignes** de 264 champs de 6 bits, ce qui colle exactement à `$numLength = 264*30 + 265*5`), empile les 5 lignes par colonne (`$blocks[$j]` = les 5 morceaux de 6 bits de la colonne j, soit 30 bits), puis : `Scramble(bloc, seed)` construit 30 emplacements à `"10"`, et pour i=0..29 écrit `"11"` ou `"00"` au premier emplacement libre en partant de `(i*seed) % 30` (une **permutation**, donc inversible) ; la sortie enchainee est `result_i = fun_i XOR result_{i-1} XOR randoms_i`. On récupère donc `fun_i = result_i XOR result_{i-1} XOR randoms_i` avec `randoms[i] = ((i+1)*327 % 681 + 344) % 313`, on vérifie que chaque fun (60 bits) ne contient que des paires 11/00 (0 non conforme -> validation), puis on inverse la permutation avec `seeds[i] = ((i+1)*127) % 500`. Les 30 lignes resultantes se lisent en ASCII : `academy{2018highw@y_2_pow3r$hel!}` (les lignes en 0x9e.. sont la même chaîne XOR 0xff).

## Flag

```
academy{2018highw@y_2_pow3r$hel!}
```

## Scripts

- [`solve.py`](../../solve/119/solve.py)
- *7 variantes intermediaires dans `solve/119/archive/`*
