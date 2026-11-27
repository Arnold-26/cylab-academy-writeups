# HideToSee

**Catégorie** : Cryptography · **Challenge** : #351 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **steghide + atbash**.

`steghide extract -sf atbash.jpg` (sans mot de passe) extrait `encrypted.txt` qui contient `zxzwvnb{zgyzhs_xizxp_zz003u7z}` : du **Atbash** (a<->z). Decode -> `academy{atbash_crack_aa003f7a}`.

## Flag

```
academy{atbash_crack_aa003f7a}
```

## Ce qu'il faut retenir

steghide exige une passphrase : elle est souvent dans les metadonnees.
