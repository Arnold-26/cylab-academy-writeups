# reverse_cipher

**Catégorie** : Reverse Engineering · **Challenge** : #79 · **Résolu le** : 2026-11-24

## Énoncé

> We have recovered a [binary](https://challenge-files.cylabacademy.net/library/4de47cc73b1c6e4976e058249b7181cfe15c64e28b5a4a0a54edefdf6608f118/rev) and a [text file](https://challenge-files.cylabacademy.net/library/4de47cc73b1c6e4976e058249b7181cfe15c64e28b5a4a0a54edefdf6608f118/rev_this). Can you reverse the flag.

## Résolution

Méthode : **inversion de transformation**.

Le binaire lit `flag.txt` et écrit `rev_this` : les 8 premiers caractères sont inchangés, puis pour i de 8 a 22 les positions **paires sont incrementees de 5** et les **impaires decrementees de 2** ; le dernier caractère est inchangé. On inverse simplement l'opération.

## Flag

```
academy{r3v3rs397436647}
```
