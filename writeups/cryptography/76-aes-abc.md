# AES-ABC

**Catégorie** : Cryptography · **Challenge** : #76 · **Résolu le** : 2026-11-24

## Énoncé

> AES-ECB is bad, so I rolled my own cipher block chaining mechanism - Addition Block Chaining!
> You can find the source here: [aes-abc.py](https://challenge-files.cylabacademy.net/library/14ceae892617d933542da8acd132767238cc50c7a66a12aaa64bf045c80dfece/aes-abc.py). The AES-ABC flag is [body.enc.ppm](https://challenge-files.cylabacademy.net/library/14ceae892617d933542da8acd132767238cc50c7a66a12aaa64bf045c80dfece/body.enc.ppm)

## Résolution

Méthode : **inversion du chainage ABC (addition mod 2^128)**.

Le mode custom ajoute le bloc chiffre précédent au bloc courant (mod 2^128). On inverse en soustrayant : `n_curr = (curr - prev) mod 2^128` en parcourant les blocs. Le resultat est toujours du **AES-ECB** (clé inconnue), mais ECB preserve les motifs : les zones uniformes de l'image donnent des blocs identiques, donc le texte du flag reste lisible dans le PPM.

## Flag

```
academy{d0Nt_r0ll_yoUr_0wN_aES}
```

## Scripts

- [`solve.py`](../../solve/76/solve.py)
