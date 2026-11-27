# droids2

**Catégorie** : Reverse Engineering · **Challenge** : #63 · **Résolu le** : 2026-11-24

## Énoncé

> Find the pass, get the flag. Check out this [file](https://challenge-files.cylabacademy.net/library/b6c139c1154ec3424dbfb06907c1246c9578e6d68311ef8b9c98c0343ee356ad/two.apk).

## Résolution

Méthode : **reassemblage smali + XOR natif (helper oregano)**.

`FlagstaffHill.getFlag` construit le mot de passe à partir d'un tableau de 6 noms Discworld (`weatherwax`, `ogg`, `garlick`, `nitt`, `aching`, `dismass`) indice par des opérations arithmetiques sur `v1=3` : `v2=0, v3=1, v4=2, v5=5, v6=4`, puis concatene `v0[5].v0[1].v0[0].v0[4].v0[3].v0[2]` -> **`dismass.ogg.weatherwax.aching.nitt.garlick`**. `sesame(mdp)` appelle `basil` puis `oregano` = XOR repetitif des données a 0x1a5d (0x27 octets) avec le mot de passe -> `academy{what.is.your.favourite.colour}`.

## Flag

```
academy{what.is.your.favourite.colour}
```
