# droids1

**Catégorie** : Reverse Engineering · **Challenge** : #14 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **XOR répétitif clé=mot de passe dans la lib native**.

Le mot de passe est la ressource `password` = **`opossum`**. `fenugreek(input)` appelle `nutmeg(input)` (validation) puis `anise(input)`, qui fait `unscramble(data@0x1a3e, 0x1e, strdup(input), strlen(input))` : **la cle du XOR est l'input lui-meme**. Avec `opossum` on obtient `academy{pining.for.the.fjords}`.

## Flag

```
academy{pining.for.the.fjords}
```

## Ce qu'il faut retenir

—
