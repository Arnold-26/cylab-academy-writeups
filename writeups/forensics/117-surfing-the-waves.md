# Surfing the Waves

**Catégorie** : Forensics · **Challenge** : #117 · **Résolu le** : 2026-11-25

## Énoncé

> main.wav (2736 echantillons, 2736 Hz)

## Résolution

Méthode : **hexadecimal encode dans les echantillons audio (2 derniers chiffres = bruit)**.

`main.wav` fait **1 seconde, mono, 2736 Hz, 2736 echantillons**, avec des valeurs comprises entre 1000 et 8509. Le spectrogramme ne montre aucun texte : la donnee n'est pas dans le domaine frequentiel. La cle est dans les **valeurs des echantillons** : en tronquant les **deux derniers chiffres** de chaque valeur (qui sont du bruit aleatoire ajoute), il ne reste que **16 valeurs uniques** — 10, 15, 20, ... 85 — soit exactement un alphabet hexadecimal de 16 symboles. En les triant et en les faisant correspondre a `0123456789abcdef` (10->0, 15->1, ... 85->f), on obtient une longue chaine hexadecimale qui se decode en ASCII comme un **programme Python generateur** : `hex_stuff[i] = 1000 + int(hex_stuff[i]) * 500 + (10 * random())` — ce qui explique parfaitement les valeurs observees (1000 + 500*n + bruit) et confirme la theorie. Le programme se termine par le drapeau en commentaire. Verification croisee : 1000 + 500*0 = 1000 et 1000 + 500*15 = 8500, coherents avec min=1000 et max=8509.

## Flag

```
academy{mU21C_1s_1337_63f2299a}
```

## Ce qu'il faut retenir

—

## Scripts

- [`solve.py`](../../solve/117/solve.py)
- *5 variantes intermediaires dans `solve/117/archive/`*
