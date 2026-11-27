# Weird File

**Catégorie** : Forensics · **Challenge** : #101 · **Résolu le** : 2026-11-24

## Énoncé

> What could go wrong if we let Word documents run programs? (aka "in-the-clear").
> [weird.docm](https://challenge-files.cylabacademy.net/library/b99ccd7c322df5b671439cb3a077a65446b967013fe4a3036610b53e0d311bca/weird.docm)

## Résolution

Méthode : **macro VBA en base64**.

Le `.docm` contient un `vbaProject.bin` dont la macro appelle `Shell("python -c 'print(...)'")` avec une chaîne **base64** : `YWNhZGVteXttNGNyMHNfcl9kNG5nM3IwdXN9` se decode en flag.

## Flag

```
academy{m4cr0s_r_d4ng3r0us}
```

## Scripts

- [`solve.py`](../../solve/101/solve.py)
