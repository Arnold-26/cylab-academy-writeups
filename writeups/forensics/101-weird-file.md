# Weird File

**Catégorie** : Forensics · **Challenge** : #101 · **Résolu le** : 2026-11-24

## Résolution

Méthode : **macro VBA en base64**.

Le `.docm` contient un `vbaProject.bin` dont la macro appelle `Shell("python -c 'print(...)'")` avec une chaine **base64** : `YWNhZGVteXttNGNyMHNfcl9kNG5nM3IwdXN9` se decode en flag.

## Flag

```
academy{m4cr0s_r_d4ng3r0us}
```

## Scripts

- [`solve.py`](../../solve/101/solve.py)
- *2 variantes intermediaires dans `solve/101/archive/`*
