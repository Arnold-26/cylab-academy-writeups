# HideToSee

**Catégorie** : Cryptography · **Challenge** : #351 · **Résolu le** : 2026-11-23

## Énoncé

> How about some hide and seek heh?
> Look at this image [here](https://challenge-files.cylabacademy.net/library/8033762450472ffeea8ef74c4098556d749abc1f4e836b849798e18e9554e5e5/atbash.jpg).

## Résolution

Méthode : **steghide + atbash**.

`steghide extract -sf atbash.jpg` (sans mot de passe) extrait `encrypted.txt` qui contient `zxzwvnb{zgyzhs_xizxp_zz003u7z}` : du **Atbash** (a<->z). Decode -> `academy{atbash_crack_aa003f7a}`.

## Flag

```
academy{atbash_crack_aa003f7a}
```

## Ce qu'il faut retenir

steghide exige une passphrase : elle est souvent dans les metadonnees.
