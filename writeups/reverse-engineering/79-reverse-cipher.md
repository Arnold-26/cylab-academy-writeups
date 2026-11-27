# reverse_cipher

**Catégorie** : Reverse Engineering · **Challenge** : #79 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **inversion de transformation**.

Le binaire lit `flag.txt` et ecrit `rev_this` : les 8 premiers caracteres sont inchanges, puis pour i de 8 a 22 les positions **paires sont incrementees de 5** et les **impaires decrementees de 2** ; le dernier caractere est inchange. On inverse simplement l'operation.

## Flag

```
academy{r3v3rs397436647}
```

## Ce qu'il faut retenir

—
