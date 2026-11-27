# Picker III

**Catégorie** : Reverse Engineering · **Challenge** : #402 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **reecriture de func_table**.

`write_variable` fait `exec('global '+var_name+'; '+var_name+' = '+value)` sans verifier le nom. On ecrit `func_table` avec une valeur de 128 caracteres dont le premier champ est `win` : `'w'+'in'+' '*29+'A'*96`. Ensuite l'option 1 appelle `call_func(0)` -> `eval('win()')`.

## Flag

```
academy{7h15_15_wh47_w3_g37_w17h_u53r5_1n_ch4rg3_3350bb13}
```

## Ce qu'il faut retenir

—
