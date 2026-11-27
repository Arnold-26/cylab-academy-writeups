# droids1

**Catégorie** : Reverse Engineering · **Challenge** : #14 · **Résolu le** : 2026-11-24

## Énoncé

> Find the pass, get the flag. Check out this [file](https://challenge-files.cylabacademy.net/library/9660a88d9399f1bdcd2a86ab0cef32c7be0e82a0bbf002f68623ef7c7495f062/one.apk).

## Résolution

Méthode : **XOR répétitif clé=mot de passe dans la lib native**.

Le mot de passe est la ressource `password` = **`opossum`**. `fenugreek(input)` appelle `nutmeg(input)` (validation) puis `anise(input)`, qui fait `unscramble(data@0x1a3e, 0x1e, strdup(input), strlen(input))` : **la clé du XOR est l'input lui-même**. Avec `opossum` on obtient `academy{pining.for.the.fjords}`.

## Flag

```
academy{pining.for.the.fjords}
```

## Scripts

- [`solve.py`](../../solve/14/solve.py)
