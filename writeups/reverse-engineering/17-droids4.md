# droids4

**Catégorie** : Reverse Engineering · **Challenge** : #17 · **Résolu le** : 2026-11-24

## Énoncé

> Reverse the pass, patch the file, get the flag. Check out this [file](https://challenge-files.cylabacademy.net/library/6a4e0bef83d40ea9121009c5ae6a5230e06eb011eef934798704fa66bcfc84f0/four.apk).

## Résolution

Méthode : **emulation du StringBuilder + XOR natif**.

`FlagstaffHill.getFlag` reconstruit le mot de passe avec quatre `StringBuilder` initialises à `aaa` (ace/jack/queen/king) et des `setCharAt` qui AJOUTENT des constantes : ace +0x13/+0x12, jack +7/0/+1, queen +0/+0xb/+0xf, king +0xe/+0x14/+0xf, puis concatene `queen+jack+ace+king` -> **`alphabetsoup`** (sans espace). Le flag vient de `pepper()` = XOR repetitif des données a 0x1aa0 (31 octets) avec la clé = le mot de passe. Piege : avec `alphabet soup` (avec espace) on obtient `academy{` correct sur 8 octets puis du bruit, ce qui fait croire à un mauvais chemin.

## Flag

```
academy{not.particularly.silly}
```

## Scripts

- [`solve.py`](../../solve/17/solve.py)
