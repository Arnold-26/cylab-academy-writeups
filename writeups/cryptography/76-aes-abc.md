# AES-ABC

**Catégorie** : Cryptography · **Challenge** : #76 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **inversion du chainage ABC (addition mod 2^128)**.

Le mode custom ajoute le bloc chiffre precedent au bloc courant (mod 2^128). On inverse en soustrayant : `n_curr = (curr - prev) mod 2^128` en parcourant les blocs. Le resultat est toujours du **AES-ECB** (cle inconnue), mais ECB preserve les motifs : les zones uniformes de l'image donnent des blocs identiques, donc le texte du flag reste lisible dans le PPM.

## Flag

```
academy{d0Nt_r0ll_yoUr_0wN_aES}
```

## Ce qu'il faut retenir

—
